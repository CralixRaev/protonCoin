import {user_from_api, coin} from "/static/common_funcs.js";

function user_or_bank(data) {
    if (data.id !== 0) {
        return user_from_api(data)
    } else {
        return "ПротонБанк"
    }
}

$(document).ready(function () {
    let table = $('#transactionList').DataTable({
        language: {
            url: '/static/datatables/ru.json'
        },
        columns: [
            {data: 'id'},
            {
                data: 'from_user', render: function (data, type, row, meta) {
                    return user_or_bank(data)
                }
            },
            {
                data: 'to_user', render: function (data, type, row, meta) {
                    return user_or_bank(data)
                }
            },
            {
                data: 'amount', render: function (data, type, row, meta) {
                    return `${data} ${coin(16)}`
                }
            },
            {data: 'comment'},
            {
                data: 'creation_date', render: function (data, type, row, meta) {
                    let date = new Date(data)
                    return date.toLocaleString('ru-RU')
                }
            },
        ],
        order: [[0, "desc"]],
        orderMulti: false,
        processing: true,
        serverSide: true,
        ajax: '/api/v1/transactions/',
    });
});
