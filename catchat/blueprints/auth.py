# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, Blueprint, request, session
from flask_login import login_user, logout_user, login_required, current_user

from catchat.extensions import db
from catchat.models import User, Room, UserRoom

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat.home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember_me = request.form.get('remember', False)

        if remember_me:
            remember_me = True

        user = User.query.filter_by(email=email).first()

        if user is not None:
            if user.password_hash is None:
                flash('Please use the third party service to log in.')
                return redirect(url_for('.login'))

            if user.verify_password(password):
                login_user(user, remember_me)

                # incre 1 for all the user's rooms
                user_rooms = UserRoom.query.filter(UserRoom.user_id == user.id).all()
                for user_room in user_rooms:
                    room_id = user_room.room_id
                    room = Room.query.get(room_id)
                    room.cur_user_total += 1
                    db.session.add(room)
                db.session.commit()

                # 登录时默认第一个room
                session['room_id'] = 1

                return redirect(url_for('chat.home'))

        flash('Either the email or password was incorrect.')
        return redirect(url_for('.login'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    # decre 1 for all the user room's cur_user_total
    user_rooms = UserRoom.query.filter(UserRoom.user_id == current_user.id).all()
    for user_room in user_rooms:
        room = Room.query.get(user_room.room_id)
        room.cur_user_total -= 1
        db.session.commit()

    # delete room_id in session
    session['room_id'] = 1

    logout_user()

    return redirect(url_for('chat.home'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat.home'))

    if request.method == 'POST':
        email = request.form['email'].lower()

        user = User.query.filter_by(email=email).first()
        if user is not None:
            flash('The email is already registered, please log in.')
            return redirect(url_for('.login'))

        nickname = request.form['nickname']
        password = request.form['password']

        user = User(nickname=nickname, email=email)
        user.set_password(password)
        db.session.add(user)

        # give this user a unknown room
        user = User.query.filter_by(email=email).first()
        user_room = UserRoom(user_id=user.id, room_id=1)
        db.session.add(user_room)
        db.session.commit()

        # incre room 1's total user
        room = Room.query.get(1)
        room.user_total += 1
        db.session.commit()

        # incre 1 for all the user room's cur_user_total
        user_rooms = UserRoom.query.filter(UserRoom.user_id == user.id).all()
        for user_room in user_rooms:
            room = Room.query.get(user_room.room_id)
            room.cur_user_total += 1
            db.session.commit()

        login_user(user, remember=True)
        return redirect(url_for('chat.profile'))

    return render_template('auth/register.html')
