const ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/webp'];

$("#btnupload").click(function () {
    $("#inpupload").trigger("click");
});

$("#inpupload").change(function () {
    let input = $("#inpupload")[0]
    if (input.files.length === 1) {
        let file = input.files[0]
        if (ALLOWED_MIME_TYPES.indexOf(file.type) === -1) {
            alert('Неправильный формат файла.');
            return;
        }
        $("#avatar_form").submit();
    }
});

$("#orderBySelect").change(function () {
    let optionValue = $(this).val();
    let url = window.location.href.split("?")[0];
    if (window.location.href.indexOf("?") > 0) {
        window.location = url + "?order_by=" + optionValue;
    } else {
        window.location = url + "?order_by=" + optionValue;
    }
});

function submitWithDoNotRedirect() {
    let form = document.getElementById("achievement-form")
    document.getElementById("do_not_redirect").value = "True"
    form.submit()
}

$(document).ready(function () {
    let topTable = $('#topTable').DataTable({
        language: {
            url: '/static/datatables/ru.json'
        },
        paging: false,
        searching: false,
        columns: [
            {
                className: 'dt-control',
                orderable: false,
                data: null,
                defaultContent: '',
            }, {}, {orderable: false}, {orderable: false}, {visible: false}
        ],
        order: [1, "asc"],
    });
    $('#topTable').on('click', 'td.dt-control', function () {
        let tr = $(this).closest('tr');
        let row = topTable.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            row.child(row.data()[4]).show();
            tr.addClass('shown');
        }
    });
    $('#criteriaList').DataTable({
        language: {
            url: '/static/datatables/ru.json'
        },
        columns: [
            {data: null, visible: false},
            {data: null, visible: false},
            {data: 'basis.name'},
            {data: 'name'},
            {data: 'cost'},
        ],
        order: [[4, "desc"]],
        orderMulti: false,
        processing: true,
        serverSide: true,
        ajax: '/api/v1/criterias/',
        pageLength: 25,
        responsive: true
    });
});
