// its actually like macros, but in js funcs

export function escapeHtml(unsafe) {
    if (unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    } else {
        return ""
    }
}

export function user_full_name(data) {
    return `${escapeHtml(data.surname)} ${escapeHtml(data.name)} ${data.patronymic ? escapeHtml(data.patronymic) : ""}`
}


export function criteria_with_basis(data) {
    return `(${escapeHtml(data.basis.name)}) ${escapeHtml(data.name)}`
}



export function user_from_api(data) {
    return `<img src="${data.avatar_path}" height="32px" width="32px" class="avatar rounded-circle">
                     ${user_full_name(data)} (${data.group.stage}${escapeHtml(data.group.letter)})`
}

export function coin_icon(size = 16) {
    return `<img src="/static/coin.webp" height="${size}px" width="${size}px"
         class="coin_icon">`
}

export function coin(size = 16) {
    return `${coin_icon(size)} ПРОтоКоин`
}