function approve(row_id) {
    window.location.href = "/manage/admin/achievement/approve" + "?id=" + row_id
}

function disapprove(row_id) {
    let reason = window.prompt("Введите причину отказа")
    if (reason) {
        window.location.href = "/manage/admin/achievement/disapprove" + "?id=" + row_id + "&reason=" + reason
    } else {
        window.alert("К сожалению, причину отказа надо указать :(")
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
                    return `<img src="${data.avatar_path}" height="32px" width="32px" class="avatar rounded-circle">
                    ${data.surname} ${data.name} ${data.patronymic}`
                }
            },
            {
                data: 'criteria', render: function (data, type, row, meta) {
                    return `(${data.basis.name}) ${data.name}`
                }
            },
            {
                data: 'achievement_file_path', render: function (data, type, row, meta) {
                    return `<div class="hover_img"><a href="/webp_viewer/?path=${data}">Наведитесь, что бы посмотреть<span><img width="400rem" src="${data}"/></a></div>`
                }, orderable: false
            },
            {
                data: 'comment', orderable: false,
            },
            {
                data: 'status_translation', render: function (data, type, row, meta) {
                    let p_class = '';
                    if (row.status === 'approved') {
                        p_class = 'text-success fw-bold'
                    } else if (row.status === 'disapproved') {
                        p_class = 'text-danger fw-bold'
                    }
                    return `<p class="${p_class}">${data}</p>`
                }
            },
            {
                data: null, render: function (data, type, row, meta) {
                    return `<div class="btn-group" role="group"><button class="btn btn-success" onclick="approve('${data.id}')"><i class="bi bi-check-circle-fill"></i></button>
<button class="btn btn-danger" onclick="disapprove('${data.id}')"><i class="bi bi-x-circle-fill"></i></button>
</div>`
                }, orderable: false
            },
        ],
        order: [[0, "desc"]],
        orderMulti: false,
        processing: true,
        serverSide: true,
        ajax: '/api/v1/achievements/',
    });
});

function changeStatusFilter () {
    let status = $('#achievementsStatusFilter').val()
    if (status === undefined) {
        status = ''
    }
    $('#achievementList').DataTable().ajax.url('/api/v1/achievements/' + status).load()
}
