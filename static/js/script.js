$('#update-book-btn').on('click',function(){
    $('#update-book-form').toggle()
})

function confirmDelete(bookId) {
    if (confirm("Are you sure you want to delete this book?")) {
        window.location.href = `/book-delete/${bookId}`;
    }
}

const inputs = $("#user-profile-form input");

$("#profile-edit-btn").on("click", function () {
    inputs.removeAttr("readonly");
    $(this).addClass("d-none");
    $("#profile-update-btn, #profile-cancel-btn").removeClass("d-none");
});

$("#profile-cancel-btn").on("click", function () {
    location.reload();
});

$('#export-borrow-history-btn').on('click',function(){
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/ajax/download-history-csv', true);
    xhr.responseType = 'blob';

    xhr.onload = function() {
        if (xhr.status === 200) {
            const blob = new Blob([xhr.response], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'borrow_history.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        } else {
            alert('Error exporting borrow history. Please try again.');
        }
    };

    xhr.onerror = function() {
        alert('Error exporting borrow history. Please try again.');
    };

    xhr.send();
})