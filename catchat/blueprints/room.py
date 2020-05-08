# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, Blueprint, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import and_
from catchat.models import Room, User, UserRoom, Message
from catchat.extensions import db
from catchat.forms import SearchRoomForm, DeleteRoomForm, CreateRoomForm, EnterRoomForm


room_bp = Blueprint('room', __name__)


@room_bp.route('/create_room', methods=['POST'])
def create_room():
    if current_user.is_authenticated:
        form = CreateRoomForm()
        if form.validate_on_submit():
            room_name = form.room_name.data
            # 判定room_name是否存在
            room = Room.query.filter(and_(Room.name == room_name, Room.owner == current_user.id)).first()
            if room_name == "" or room:
                return redirect(url_for('room.get_rooms'))

            room = Room(name=room_name,
                        user_total=1,
                        cur_user_total=1,
                        owner=current_user.id)
            db.session.add(room)

            room = Room.query.filter(and_(Room.name == room_name, Room.owner == current_user.id)).first()
            user_room = UserRoom(user_id=current_user.id,
                                 room_id=room.id)
            db.session.add(user_room)
            db.session.commit()

            return redirect(url_for('room.get_rooms'))

    return render_template('auth/login.html')


@room_bp.route('/delete_room/<int:room_id>', methods=['POST'])
def delete_room(room_id):
    room = Room.query.get(room_id)
    # judge if current_user.id is valid
    if room.owner != current_user.id:
        flash("You aren't the owner of this room!")
        return redirect(url_for('room.get_rooms'))

    db.session.delete(room)

    user_rooms = UserRoom.query.filter(UserRoom.room_id == room_id).all()
    for user_room in user_rooms:
        db.session.delete(user_room)

    db.session.commit()
    flash('Your room is deleted!')

    return redirect(url_for('room.get_rooms'))


@room_bp.route('/get_rooms', methods=['GET'])
def get_rooms():
    # return all the rooms the current user has
    user_rooms = UserRoom.query.filter(UserRoom.user_id == current_user.id).all()
    rooms = []
    for user_room in user_rooms:
        room = Room.query.filter(user_room.room_id == Room.id).first()
        user = User.query.get(room.owner)
        data = {
            'room_id':   room.id,
            'room_name': room.name,
            'user_total': room.user_total,
            'cur_user_total': room.cur_user_total,
            'owner': user.nickname,
        }
        rooms.append(data)
    username = User.query.get_or_404(current_user.id).nickname

    search_form = SearchRoomForm()
    delete_form = DeleteRoomForm()
    create_form = CreateRoomForm()
    enter_form = EnterRoomForm()
    return render_template(
        'room/room.html', username=username, rooms=rooms,
        searchform=search_form, deleteform=delete_form, createform=create_form, enter_form=enter_form)


@room_bp.route('/search_room', methods=['POST'])
def search_room():
    search_form = SearchRoomForm()
    if search_form.validate_on_submit():
        room_name = search_form.room_name.data
        rooms = Room.query.filter(Room.name.like('%{}%'.format(room_name))).all()
        datas = []
        for room in rooms:
            user = User.query.get(room.owner)
            data = {
                'room_id': room.id,
                'room_name': room.name,
                'cur_user_total': room.cur_user_total,
                'user_total': room.user_total,
                'owner': user.nickname,
            }
            datas.append(data)

        enter_form = EnterRoomForm()
        return render_template('room/search.html', rooms=datas, enter_form=enter_form)
    return redirect(url_for('room.get_rooms'))


@room_bp.route('/enter_room/<int:room_id>', methods=['POST'])
def enter_room(room_id):
    enter_form = EnterRoomForm()
    if enter_form.validate_on_submit():
        amount = current_app.config['CATCHAT_MESSAGE_PER_PAGE']
        messages = Message.query.filter_by(room_id=room_id).order_by(Message.timestamp.asc())[-amount:]
        user_amount = User.query.count()
        room = Room.query.get(room_id)
        return render_template('chat/home.html', messages=messages, user_amount=user_amount, room=room)
    return redirect(url_for('room.get_rooms'))


@room_bp.route('/edit_room/<int:room_id>', methods=['POST'])
def edit_room(room_id):
    pass


@room_bp.route('/add_member/<int:user_id>/<int:room_id>', methods=['POST'])
def add_member(user_id, room_id):
    pass


@room_bp.route('/delete_member/<int:user_id>/<int:room_id>', methods=['POST'])
def delete_member(user_id, room_id):
    pass
