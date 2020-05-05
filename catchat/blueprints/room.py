# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user
from catchat.models import Room, User, UserRoom, Message
from catchat.extensions import db

room_bp = Blueprint('room', __name__)


@room_bp.route('/create_room/<string:room_name>', methods=['POST'])
def create_room(room_name="未命名聊天室"):
    if current_user.is_authenticated:
        room = Room(name=room_name,
                    user_total=1,
                    cur_user_total=1)
        db.session.add(room)

        user_room = UserRoom(user_id=current_user.id,
                             room_id=room.id)
        db.session.add(user_room)
        db.commit()

        # return all the rooms the current user has
        user_rooms = UserRoom.query.filter(UserRoom.user_id == current_user.id).all()
        rooms = []
        for user_room in user_rooms:
            rooms.append(Room.query.filter(user_room.room_id == Room.id).first())

        return render_template('room/room.html', rooms=rooms)

    return render_template('auth/login.html')


@room_bp.route('/delete_room/<int:room_id>', methods=['PUT'])
def delete_room():

    return redirect(url_for('chat.home'))


@room_bp.route('/get_rooms', methods=['GET'])
def get_rooms():
    # return all the rooms the current user has
    user_rooms = UserRoom.query.filter(UserRoom.user_id == current_user.id).all()
    rooms = []
    for user_room in user_rooms:
        rooms.append(Room.query.filter(user_room.room_id == Room.id).first())

    return render_template('room/room.html', rooms=rooms)


@room_bp.route('/add_member/<int:user_id>/<int:room_id>', methods=['POST'])
def add_member(user_id, room_id):
    pass
