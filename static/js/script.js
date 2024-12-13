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