import {user_from_api} from "/static/common_funcs.js";

function format(data) {
    let html = []
    html.push(`<a href="/manage/methods/user/new_password?id=${data.id}&back=${window.location.href}" class="btn btn-primary btn-sm me-1" role="button" data-toggle="button">Сгенирировать новый пароль</a>`)
    html.push("<a href=\"/manage/admin/users/edit/?id=" + data.id + "\" class=\"btn btn-primary btn-sm me-1\" role=\"button\" data-toggle=\"button\">Редактировать пользователя</a>")
    html.push(`<a href="/manage/methods/user/delete?id=${data.id}&back=${window.location.href}" class="btn btn-danger btn-sm me-1" role="button" data-toggle="button">Удалить пользователя</a>`)
    return html
}

$(document).ready(function () {
    let table = $('#userList').DataTable({
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
                data: 'null', render: function (data, type, row, meta) {
                    return `${user_from_api(row)}`
                }
            },
            {
                data: null, render: function (data, type, row, meta) {
                    return data.group.stage + data.group.letter
                }
            },
            {data: 'balance.amount'},
        ],
        order: [[0, "desc"]],
        orderMulti: false,
        processing: true,
        serverSide: true,
        ajax: '/api/v1/users/',
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

});

