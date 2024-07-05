from flask import Flask, render_template, request, jsonify
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import numpy as np

app = Flask(__name__)
app.static_folder = 'static'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/suggest_movie', methods=['GET'])
def suggest_movie():
    search_query = request.args.get('q', '')
    
    if search_query:
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT title FROM movies WHERE title LIKE ? LIMIT 10", (f'%{search_query}%',))
        results = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return jsonify(results)
    
    return jsonify([])

@app.route('/movie_detail')
def movie_detail():
    title = request.args.get('title')
    if title:
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM movies WHERE title = ?", (title,))
        movie = cursor.fetchone()
        
        # conn.close()
        
        cursor.execute("SELECT * FROM movies ")
        movies = cursor.fetchall()
        conn.close()

        if movies:
            netflix_data = pd.DataFrame(movies, columns=['id','type','name', 'creator', 'starring', 'year', 'rating', 'time', 'genres', 'country', 'describle'])
            recommend_name = get_recommendations(movie[2], netflix_data).tolist()
            return render_template('movie_detail.html', recommend_name=recommend_name, movie = movie)

    
    return "Không tìm thấy thông tin cho bộ phim này."

def get_recommendations(title, netflix_data):
    tfidf = TfidfVectorizer(stop_words='english')
    netflix_data['describle'] = netflix_data['describle'].fillna('')
    tfidf_matrix = tfidf.fit_transform(netflix_data['describle'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(netflix_data.index, index=netflix_data['name']).drop_duplicates()
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return netflix_data['name'].iloc[movie_indices]

if __name__ == '__main__':
    app.run()

