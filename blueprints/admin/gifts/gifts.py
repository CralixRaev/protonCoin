import os.path

import flask
from flask import Blueprint, render_template, redirect, request, url_for, Request, Response
from flask_login import login_required
from werkzeug.datastructures import MultiDict

from blueprints.admin.gifts.forms.gift import GiftForm
from blueprints.admin.users.forms.user import UserForm
from db.models.gift import GiftQuery
from db.models.group import GroupQuery
from db.models.user import UserQuery
from uploads import gift_images
from util import admin_required

gifts = Blueprint('gifts', __name__, template_folder='templates')


@gifts.route('/')
@login_required
@admin_required
def index():
    context = {
        'title': 'Подарки',
        'gifts': GiftQuery.get_all_gifts()
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
        filename = gift_images.save(image)
        gift = GiftQuery.create_gift(form.name.data, form.description.data, form.price.data,
                                     filename)
        flask.flash(f"Подарок успешно создан")
        return redirect(url_for('admin.gifts.index'))
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
        image = form.image.data
        filename = gift_images.save(image)
        gift = GiftQuery.update_gift(gift, form.name.data, form.description.data, form.price.data,
                                     filename)
        flask.flash(f"Подарок успешно обновлен")
        return redirect(url_for('admin.gifts.index'))
    context['form'] = GiftForm(MultiDict(gift.__dict__.items()))
    return render_template("gifts/gift.html", **context)
