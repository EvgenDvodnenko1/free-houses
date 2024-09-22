from flask import render_template, request, redirect, url_for
from models import Config, User
from helpers import UserId, check_form


def authorize_page():
    return render_template('auth.html')


def sign_up_page():
    return render_template('signUp.html')

def sign_up():
    check_form(request, ['name', 'age', 'phone-number', 'password'])

    phone_number = request.form.get('phone-number')
    db = Config.SESSION()
    check = db.query(User).filter_by(phone_number=phone_number).first()

    if check != None:
        return render_template('error.html', error_text='User with such phone number already exists')
    
    new_user = User(name=request.form.get('name'),
                    age=int(request.form.get('age')) if request.form.get('age') else 0,
                    phone_number=request.form.get('phone-number'),
                    password=request.form.get('password'),
                    role=request.form.get('role'))
    
    db.add(new_user)
    db.commit()
    id = db.query(User).filter_by(phone_number=phone_number).first().id
    UserId.set_user_id(id)
    db.close()

    return redirect(url_for('main'))


def log_in_page():
    return render_template('logIn.html')

def log_in():
    check_form(request, ['phone-number', 'password'])

    phone_number = request.form.get('phone-number')
    password = request.form.get('password')
    db = Config.SESSION()
    user = db.query(User).filter_by(phone_number=phone_number).first()

    if user == None:
        return render_template('error.html', error_text='User with such phone number does not exist')
    if user.password != password:
        return render_template('error.html', error_text='Incorrect password')
    
    UserId.set_user_id(user.id)

    return redirect(url_for('main'))


def update_profile_page():
    if UserId.get_user_id() == -1:
        return redirect(url_for('main'))

    db = Config.SESSION()
    user = db.query(User).get(UserId.get_user_id())
    db.close()
    return render_template('updateProfile.html', user=user)

def update_profile():
    check_form(request, ['name', 'phone-number', 'age', 'password'])

    db = Config.SESSION()
    user = db.query(User).get(UserId.get_user_id())
    user.name = request.form.get('name')
    user.age = request.form.get('age')
    user.phone_number = request.form.get('phone-number')
    user.password = request.form.get('password')
    user.role = request.form.get('role')
    db.commit()
    db.close()

    return redirect(url_for('main'))


def log_out():
    UserId.set_user_id(-1)
    return redirect(url_for('main'))