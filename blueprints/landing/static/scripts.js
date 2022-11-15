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