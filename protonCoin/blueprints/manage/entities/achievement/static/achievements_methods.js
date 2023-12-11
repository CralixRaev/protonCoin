function approve(row_id) {
    window.location.href = `/manage/methods/achievement/approve?id=${row_id}&back=${window.location.href}`
}

function disapprove(row_id) {
    let reason = window.prompt("Введите причину отказа")
    if (reason) {
        window.location.href = `/manage/methods/achievement/disapprove?id=${row_id}&reason=${reason}&back=${window.location.href}`
    } else {
        window.alert("К сожалению, причину отказа надо указать :(")
    }
}


function disapprove_existing(row_id) {
    let reason = window.prompt("Введите причину отклонения существующего достижения")
    if (reason) {
        window.location.href = `/manage/methods/achievement/disapprove_existing?id=${row_id}&reason=${reason}&back=${window.location.href}`
    } else {
        window.alert("К сожалению, причину отклонения надо указать :(")
    }
}
