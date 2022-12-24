import {criteria_with_basis, escapeHtml, user_from_api, user_full_name} from "/static/common_funcs.js";


function redrawTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
}

function approved_disapproved_user(data) {
    if (data && data.id !== 0) {
        return user_full_name(data)
    } else {
        return `пока что никто`
    }
}

$(document).ready(function () {
    let table = $('#achievementList').DataTable({
        language: {
            url: '/static/datatables/ru.json'
        },
        columns: [
            {data: 'id'},
            {
                data: 'user', render: function (data, type, row, meta) {
                    return `${user_from_api(data)}`
                }
            },
            {
                data: 'criteria', render: function (data, type, row, meta) {
                    return criteria_with_basis(data)
                }
            },
            {
                data: 'achievement_file_path', render: function (data, type, row, meta) {
                    return `<div class="hover_img"><a href="/webp_viewer/?path=${data}">Наведитесь, что бы посмотреть<span><img width="400rem" src="${data}"/></a></div>`
                }, orderable: false
            },
            {
                data: 'comment', orderable: false, render: $.fn.dataTable.render.text()
            },
            {
                data: 'status_translation', render: function (data, type, row, meta) {
                    let p_class = '';
                    if (row.status === 'approved') {
                        p_class = 'text-success fw-bold'
                    } else if (row.status === 'disapproved') {
                        p_class = 'text-danger fw-bold'
                    }
                    return `<a class="${p_class}" data-bs-toggle="tooltip" data-bs-title="${escapeHtml(row.disapproval_reason) ?? ' '}, изменил ${approved_disapproved_user(row.approved_disapproved_user)}">${data}</a>`
                }
            },
            {
                data: null, render: function (data, type, row, meta) {
                    let html = []
                    html.push(`<div class="btn-group" role="group">`)
                    if (row.status === 'approved') {
                    } else if (row.status === 'awaiting_approval') {
                        html.push(`<button class="btn btn-success" onclick="approve('${data.id}')"><i class="bi bi-check-circle-fill"></i></button>`)
                        html.push(`<button class="btn btn-danger" onclick="disapprove('${data.id}')"><i class="bi bi-x-circle-fill"></i></button>`)
                    }
                    html.push(`</div>`)
                    return html.join('')
                }, orderable: false
            },
        ],
        order: [[5, "asc"]],
        orderMulti: false,
        processing: true,
        serverSide: true,
        ajax: {url: '/api/v1/achievements/', data: {'is_teacher': 'true'}},
        "rowCallback": function (row, data, index) {
            if (data.status === 'disapproved') {
                $('td', row).addClass('table-danger');
            } else if (data.status === 'approved') {
                $('td', row).addClass('table-success');
            }
        },
        "drawCallback": redrawTooltips,
    });
    $('#achievementsStatusFilter').on('change', function () {
        console.log("print")
        let status = this.value
        if (status === undefined) {
            status = ''
        }
        $('#achievementList').DataTable().ajax.url('/api/v1/achievements/' + status).load()

    })
});
