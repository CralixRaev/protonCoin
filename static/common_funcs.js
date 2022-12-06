// its actually like macros, but in js funcs

export function user_from_api(data) {
    return `<img src="${data.avatar_path}" height="32px" width="32px" class="avatar rounded-circle">
                    ${data.surname} ${data.name} ${data.patronymic} (${data.group.stage}${data.group.letter})`
}

export function coin_icon(size = 16) {
    return `<img src="/static/coin.webp" height="${size}px" width="${size}px"
         class="coin_icon">`
}

export function coin(size = 16) {
    return `${coin_icon(size)} ПРОтоКоин`
}