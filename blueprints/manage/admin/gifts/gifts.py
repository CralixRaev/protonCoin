import flask
from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required
from werkzeug.datastructures import MultiDict, FileStorage

from blueprints.manage.admin.gifts.forms.gift import GiftForm
from db.models.gift import GiftQuery
from uploads import gift_images
from util import admin_required, save_upload

gifts = Blueprint('gifts', __name__, template_folder='templates', static_folder='static')


@gifts.route('/')
@login_required
@admin_required
def index():
    context = {
        'title': 'Подарки',
    }
    return render_template("gifts/gifts.html", **context)


@gifts.route('/create/', methods=['GET', 'POST'])
@login_required
@admin_required
def create_gift():
    form = GiftForm()
    context = {
        'title': 'Создать подарок',
        'form': form
    }
    if form.validate_on_submit():
        image = form.image.data
        filename = save_upload(image, gift_images)
        gift = GiftQuery.create_gift(form.name.data, form.description.data, form.price.data,
                                     filename, form.promo_price.data)
        flask.flash(f"Подарок успешно создан", "success")
        return redirect(url_for('manage.admin.gifts.index'))
    return render_template("gifts/gift.html", **context)


@gifts.route('/edit/', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_gift():
    gift = GiftQuery.get_gift_by_id(request.args.get('id'))
    form = GiftForm()
    context = {
        'title': 'Редактировать подарок',
        'form': form
    }
    if form.validate_on_submit():
        filename = None
        image = form.image
        if image.data:
            filename = save_upload(image.data, gift_images)
        gift = GiftQuery.update_gift(gift, form.name.data, form.description.data, form.price.data,
                                     filename, form.stock.data, form.promo_price.data)
        flask.flash(f"Подарок успешно обновлен", "success")
        return redirect(url_for('manage.admin.gifts.index'))
    context['form'] = GiftForm(MultiDict(gift.__dict__.items()))
    return render_template("gifts/gift.html", **context)


@gifts.route('/delete/')
@login_required
@admin_required
def delete_gift():
    gift_id = request.args.get("id")
    gift = GiftQuery.get_gift_by_id(gift_id)
    GiftQuery.delete_gift(gift)
    flask.flash(f"Подарок ID: {gift.id} - {gift.name} успешно удалён", "success")
    return redirect(url_for('manage.admin.gifts.index'))
