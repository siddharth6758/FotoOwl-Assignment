$('#update-book-btn').on('click',function(){
    $('#update-book-form').toggle()
})

function confirmDelete(bookId) {
    if (confirm("Are you sure you want to delete this book?")) {
        window.location.href = `/delete-book/${bookId}/`;
    }
}