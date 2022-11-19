function format(data) {
    let html = []
    html.push("<a href=\"/manage/admin/groups/edit/?id=" + data.id + "\" class=\"btn btn-primary btn-sm me-1\" role=\"button\" data-toggle=\"button\">Редактировать класс</a>")
    html.push("<a href=\"/manage/admin/groups/delete/?id=" + data.id + "\" class=\"btn btn-danger btn-sm me-1\" role=\"button\" data-toggle=\"button\">Удалить класс</a>")
    return html
}

$(document).ready(function () {
    table = $('#groupList').DataTable({
        language: {
            url: '/static/datatables/ru.json'
        },
        columns: [
            {
                className: 'dt-control',
                orderable: false,
                data: null,
                defaultContent: '',
            },
            {data: 'id'},
            {
                data: 'name', render: function (data, type, row, meta) {
                    return row.stage + row.letter
                }
            },
        ],
        order: [[1, "desc"]],
        orderMulti: false,
        processing: true,
        serverSide: true,
        ajax: '/api/v1/groups/',
    });
});

$('#groupList').on('click', 'td.dt-control', function () {
    let tr = $(this).closest('tr');
    let row = table.row(tr);

    if (row.child.isShown()) {
        // This row is already open - close it
        row.child.hide();
        tr.removeClass('shown');
    } else {
        // Open this row
        row.child(format(row.data())).show();
        tr.addClass('shown');
    }
});
