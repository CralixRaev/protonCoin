import {user_from_api, coin} from "/static/common_funcs.js";

function format(data) {
    let html = []
    html.push(`<div class="container">
        <div class="row">
            <div class="col">Предпросмотр:
                <div class="card" style="width: 18rem;">
                    <img class="card-img-top" src="${data.image_file}" alt="${data.name}">
                    <div class="card-body">
                        <h5 class="card-title">${data.name}</h5>
                        <p class="card-text">${data.description}</p>
                        <div class="d-flex justify-content-between align-items-center mt-auto">
                            <div class="btn-group">
                                <a href="#" class="btn btn-sm btn-primary" role="button">Купить</a>
                            </div>
                            <small class="text-right">${data.price} ${coin()}</small>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col">
                <a href="/manage/admin/gifts/edit/?id=${data.id}" class="btn btn-primary btn-sm me-1"
                   role="button"
                   data-toggle="button">Редактировать подарок</a>
                <a href="/manage/admin/gifts/delete/?id=${data.id}" class="btn btn-danger btn-sm me-1"
                   role="button" data-toggle="button">Удалить подарок</a>
            </div>
        </div>
    </div>`)
    return html
}

$(document).ready(function () {
    let table = $('#giftList').DataTable({
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
            {data: 'name'},
            {
                data: 'price', render: function (data, type, row, meta) {
                    return `${data} ${coin(16)}`
                }
            },
        ],
        order: [[3, "desc"]],
        orderMulti: false,
        processing: true,
        serverSide: true,
        ajax: '/api/v1/gifts/',
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
