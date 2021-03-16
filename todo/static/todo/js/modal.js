const tasks = document.getElementsByClassName("fillform");

for(var i = 0; i < tasks.length; i++){
    tasks[i].addEventListener("click", function() {
        let data = {};
        data = {
                "title": this.getAttribute("data-title"),
                "description": this.getAttribute("data-description"),
                "id": this.getAttribute("data-id"),
                "important": this.getAttribute("data-important"),
                "completed": this.getAttribute("data-completed"),
            }
        console.log(data)
        $('#updationModal').on('show.bs.modal', function () {
                $('#updation-title').val(data.title);
                $('#updation-description-text').val(data.description);
                $('#pk').val(data.id);
                $('#updation-customCheck1').prop('checked', data.important=="True");
                $('#updation-customCheck2').prop('checked', data.completed=="True");
        })
})}

document.getElementById("clearform").addEventListener("click", function() {
    $('#creationModal').on('show.bs.modal', function () {
                $('#creation-title').val("");
                $('#creation-description-text').val("");
                $('#creation-customCheck1').prop('checked', false);
                $('#creation-customCheck2').prop('checked', false);

        })
})