$(function() {


$("form[type='ajax']").on("submit", function(e) {
    
    e.preventDefault();
    $.post(this.action, $(this).serialize());
    
    var f = e.target,
        formData = new FormData(f),
        xhr = new XMLHttpRequest();
     
    xhr.open("POST", f.action);
    xhr.send(formData);
});


});