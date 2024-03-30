<?php
// Kết nối đến cơ sở dữ liệu MySQL (đảm bảo rằng bạn đã cài đặt và cấu hình cơ sở dữ liệu MySQL trước)
$servername = "localhost";
$username = "root";
$password = "0398025073oK";
$dbname = "NETFLIX";

// Tạo kết nối đến cơ sở dữ liệu
$conn = new mysqli($servername, $username, $password, $dbname);

// Kiểm tra kết nối
if ($conn->connect_error) {
    die("Connected error: " . $conn->connect_error);
}

if (isset($_GET['query'])) {
    $query = $conn->real_escape_string($_GET['query']); // Kiểm tra và tránh SQL injection

    // Truy vấn cơ sở dữ liệu để lấy danh sách gợi ý tên phim
    $sql = "SELECT name FROM netflix_full WHERE name LIKE '%" . $query . "%'";
    $result = $conn->query($sql);
    
    $suggestions = array();
    
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $suggestions[] = $row['name'];
        }
    }
    
    echo json_encode($suggestions);
}


// Đóng kết nối đến cơ sở dữ liệu
$conn->close();
?>
