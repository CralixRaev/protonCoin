function format(data) {
    let html = []
    html.push(`<a href="/manage/admin/news/edit?news_id=${data.id}" class="btn btn-primary btn-sm me-1" role="button">Редактировать новость</a>`)
    // html.push(`<a href="/manage/admin/basises/delete?id=${data.id}" class="btn btn-danger btn-sm me-1" role="button">Удалить основание</a>`)
    return html
}

$(document).ready(function () {
    table = $('#newsList').DataTable({
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
            {data: 'id', render: $.fn.dataTable.render.text()},
            {data: 'title', render: $.fn.dataTable.render.text()},
        ],
        order: [[1, "desc"]],
        orderMulti: false,
        processing: true,
        serverSide: true,
        ajax: '/api/v1/news/',
    });
});

$('#newsList').on('click', 'td.dt-control', function () {
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
