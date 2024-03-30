
document.addEventListener("DOMContentLoaded", function () {
        // Mã JavaScript ở đây
        // Lấy trường nhập và phần tử danh sách gợi ý
    var filmNameInput = document.getElementById('filmNameInput');
    var suggestionsList = document.getElementById('suggestions');

    // Gắn sự kiện "keyup" vào trường nhập
    filmNameInput.addEventListener('keyup', function() {
        // Lấy giá trị nhập từ trường nhập
        var inputText = filmNameInput.value;

        // Gửi yêu cầu đến dịch vụ back-end PHP (ví dụ: /suggest-films.php) để lấy danh sách gợi ý
        fetch(`suggest-films.php?query=${inputText}`)
            .then(response => response.json())
            .then(suggestions => {
                // Kiểm tra xem suggestions có phải là mảng hay không
                if (Array.isArray(suggestions)) {
                    // Xóa danh sách gợi ý cũ
                    while (suggestionsList.firstChild) {
                        suggestionsList.removeChild(suggestionsList.firstChild);
                    }
            
                    // Hiển thị danh sách gợi ý mới
                    suggestions.forEach(function(suggestion) {
                        var listItem = document.createElement('li');
                        listItem.textContent = suggestion;
                        suggestionsList.appendChild(listItem);
                    });
                } else {
                    // Xử lý trường hợp khi suggestions không phải là mảng
                    console.error('Invalid suggestions:', suggestions);
                }
            });
            
    });
});