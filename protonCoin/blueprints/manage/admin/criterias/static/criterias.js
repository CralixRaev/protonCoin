function format(data) {
    let html = []
    html.push("<a href=\"/manage/admin/criterias/edit/?id=" + data.id + "\" class=\"btn btn-primary btn-sm me-1\" role=\"button\" data-toggle=\"button\">Редактировать критерию</a>")
    html.push("<a href=\"/manage/admin/criterias/delete/?id=" + data.id + "\" class=\"btn btn-danger btn-sm me-1\" role=\"button\" data-toggle=\"button\">Удалить критерию</a>")
    return html
}

$(document).ready(function () {
    table = $('#criteriaList').DataTable({
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
            {data: 'basis.name', orderable: false},
            {data: 'name'},
            {data: 'cost'},
        ],
        order: [[4, "desc"]],
        orderMulti: false,
        processing: true,
        serverSide: true,
        ajax: '/api/v1/criterias/',
    });
});

$('#criteriaList').on('click', 'td.dt-control', function () {
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
