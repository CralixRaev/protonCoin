$(document).ready(function () {
    $('#achievementList').DataTable({
        language: {
            url: '/static/datatables/ru.json'
        },
        processing: true,
        serverSide: true,
        ajax: '/manage/admin/achievement/data',
    });
});