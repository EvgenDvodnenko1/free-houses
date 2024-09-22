from flask import render_template, request, redirect, url_for
from helpers import UserId, check_id, check_form
from models import Config, User, House, Job


def main():
    print(f'main ID {UserId.get_user_id()}')
    if UserId.get_user_id() == -1:
        return redirect(url_for('authorize_page'))
    return redirect(url_for('find_house_page'))


def find_house_page():
    db = Config.SESSION()
    if UserId.get_user_id() == -1:
        return redirect(url_for('main'))
    isSeller = db.query(User).get(UserId.get_user_id()).role == 'seller'
    db.close()
    return render_template('findHouse.html', isSeller=isSeller)

def find_job_page():
    db = Config.SESSION()
    if UserId.get_user_id() == -1:
        return redirect(url_for('main'))
    isSeller = db.query(User).get(UserId.get_user_id()).role == 'seller'
    db.close()
    return render_template('findJob.html', isSeller=isSeller)


def find_house():

    check_form(request, ['city'])
    city = request.form.get('city')
    pet_friendly = request.form.get('pet-friendly') == 'on'

    db = Config.SESSION()
    all_houses = db.query(House).filter_by(city=city)
    all_houses = all_houses.filter_by(pet_friendly=pet_friendly) if pet_friendly else all_houses
    db.close()

    results = [{'id': i.id,
                'city': i.city,
                'house_type': i.house_type,
                'pet_friendly': i.pet_friendly,
                'owner_name' : db.query(User).get(i.owner_id).name,
                'owner_age' : db.query(User).get(i.owner_id).age,
                'owner_phone_number' : db.query(User).get(i.owner_id).phone_number,} for i in all_houses]
    
    return render_template('houseResults.html', results=results)

def find_job():
    check_id()

    check_form(request, ['city', 'sallary'])
    city = request.form.get('city')
    sallary = request.form.get('sallary')

    db = Config.SESSION()
    all_jobs = db.query(Job).filter(Job.city.like(city), Job.sallary >= sallary)
    db.close()

    results = [{'id': i.id,
                'city': i.city,
                'name': i.name,
                'description': i.description,
                'sallary': i.sallary,
                'owner_name' : db.query(User).get(i.owner_id).name,
                'owner_age' : db.query(User).get(i.owner_id).age,
                'owner_phone_number' : db.query(User).get(i.owner_id).phone_number,} for i in all_jobs]
    
    return render_template('jobResults.html', results=results)


def my_profile_page():
    if UserId.get_user_id() == -1:
        return redirect(url_for('main'))

    db = Config.SESSION()
    user = db.query(User).get(UserId.get_user_id())
    db.close()

    user = {'id': user.id,
            'name': user.name,
            'age': user.age,
            'user_role': user.role,
            'phone_number': user.phone_number}

    return render_template('myProfile.html', user=user)