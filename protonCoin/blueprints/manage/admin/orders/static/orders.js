import {user_from_api, coin} from "/static/common_funcs.js";

$(document).ready(function () {
    let table = $('#orderList').DataTable({
        language: {
            url: '/static/datatables/ru.json'
        },
        columns: [
            {data: 'id'},
            {data: 'gift.name'},
            {data: 'status_translation'},
            {
                data: 'user', render: function (data, type, row, meta) {
                    return `${user_from_api(data)}`
                }
            },
            {
                data: 'creation_date', render: function (data, type, row, meta) {
                    let date = new Date(data)
                    return date.toLocaleString('ru-RU')
                }
            },
            {
                data: null, render: function (data, type, row, meta) {
                    let html = []
                    html.push(`<div class="btn-group" role="group">`)
                    if (row.status === 'created') {
                        html.push(`<a class="btn btn-success" type="button" href="/manage/admin/orders/deliver/${row.id}"><i class="bi bi-check-circle-fill"></i></a>`)
                        html.push(`<a class="btn btn-danger" type="button" href="/manage/admin/orders/cancel/${row.id}"><i class="bi bi-x-circle-fill"></i></a>`)
                    }
                    html.push(`</div>`)
                    return html.join('')
                }, orderable: false
            }
        ],
        order: [[0, "desc"]],
        orderMulti: false,
        processing: true,
        serverSide: true,
        ajax: '/api/v1/orders/',
    });

    $('#giftList').on('click', 'td.dt-control', function () {
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
