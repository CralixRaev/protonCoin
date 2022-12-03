function format(data) {
    let html = []
    html.push(`<a href="/manage/methods/user/new_password?id=${data.id}&back=${window.location.href}" class="btn btn-primary btn-sm me-1" role="button" data-toggle="button">Сгенирировать новый пароль</a>`)
    return html
}

$(document).ready(function () {
    table = $('#userList').DataTable({
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
                data: null, render: function (data, type, row, meta) {
                    return `<img src="${data.avatar_path}" height="32px" width="32px" class="avatar rounded-circle">
                    ${data.surname} ${data.name} ${data.patronymic}`
                }
            },
            {
                data: null, render: function (data, type, row, meta) {
                    return data.group.stage + data.group.letter
                }
            },
            {data: 'balance.amount'},
        ],
        order: [[2, "asc"]],
        orderMulti: false,
        processing: true,
        serverSide: true,
        ajax: {url: '/api/v1/users/', data: {
            'is_teacher': 'true'
            }},
    });
});

$('#userList').on('click', 'td.dt-control', function () {
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
