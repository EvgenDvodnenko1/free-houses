from flask import render_template, redirect,url_for , request
from models import Config, User, House, Job
from helpers import UserId, check_form, check_id

def all_houses_page():
    check_id()

    db = Config.SESSION()
    all_houses = db.query(House).all()

    results = [{'id': i.id,
                'city': i.city,
                'house_type': i.house_type,
                'pet_friendly': i.pet_friendly,
                'owner_name' : db.query(User).get(i.owner_id).name,
                'owner_age' : db.query(User).get(i.owner_id).age,
                'owner_phone_number' : db.query(User).get(i.owner_id).phone_number} for i in all_houses]
    
    db.close()
    return render_template('allHouses.html', results=results)

def all_jobs_page():
    check_id()

    db = Config.SESSION()
    all_jobs = db.query(Job).all()

    results = [{'id': i.id,
                'city': i.city,
                'name': i.name,
                'description': i.description,
                'sallary': i.sallary,
                'owner_name' : db.query(User).get(i.owner_id).name,
                'owner_age' : db.query(User).get(i.owner_id).age,
                'owner_phone_number' : db.query(User).get(i.owner_id).phone_number} for i in all_jobs]
    
    db.close()
    return render_template('allJobs.html', results=results)


def my_offers_page():
    check_id()

    db = Config.SESSION()

    all_houses = db.query(House).filter_by(owner_id=UserId.get_user_id())
    all_houses = [{'id': i.id,
                'city': i.city,
                'house_type': i.house_type,
                'pet_friendly': i.pet_friendly,
                'owner_name' : db.query(User).get(i.owner_id).name,
                'owner_age' : db.query(User).get(i.owner_id).age,
                'owner_phone_number' : db.query(User).get(i.owner_id).phone_number} for i in all_houses]

    all_jobs = db.query(Job).filter_by(owner_id=UserId.get_user_id())
    all_jobs = [{'id': i.id,
                'city': i.city,
                'name': i.name,
                'description': i.description,
                'sallary': i.sallary,
                'owner_name' : db.query(User).get(i.owner_id).name,
                'owner_age' : db.query(User).get(i.owner_id).age,
                'owner_phone_number' : db.query(User).get(i.owner_id).phone_number,} for i in all_jobs]
    db.close()

    return render_template('myOffers.html', houses=all_houses, jobs=all_jobs)


def add_house_page():
    check_id()

    return render_template('addHouse.html')

def add_house():
    check_id()

    check_form(request, ['city', 'house-type'])
    city = request.form.get('city')
    pet_friendly = request.form.get('pet-friendly') == 'on'
    house_type = request.form.get('house-type')
    if UserId.get_user_id() == -1:
        return redirect(url_for('main'))
    new_house = House(  owner_id=UserId.get_user_id(),
                        city=city,
                        house_type=house_type, 
                        pet_friendly=pet_friendly)
    db = Config.SESSION()
    db.add(new_house)
    db.commit()
    db.close()

    return redirect(url_for('main'))


def add_job_page():
    check_id()

    return render_template('addJob.html')

def add_job():
    check_id()

    check_form(request, ['city', 'name', 'sallary'])
    city = request.form.get('city')
    sallary = int(request.form.get('sallary'))
    name = request.form.get('name')
    description = request.form.get('description')

    if UserId.get_user_id() == -1:
        return redirect(url_for('main'))

    new_job = Job(owner_id=UserId.get_user_id(),
                  city=city, 
                  sallary=sallary, 
                  name=name, 
                  description=description)
    db = Config.SESSION()
    db.add(new_job)
    db.commit()
    db.close()

    return redirect(url_for('main'))


def update_house_page(id):
    if UserId.get_user_id() == -1:
        return redirect(url_for('main'))
    db = Config.SESSION()
    house = db.query(House).get(id)
    db.close()
    return render_template('updateHouse.html', house=house, id=house.id)

def update_house(id):
    db = Config.SESSION()
    house = db.query(House).get(id)
    house.city = request.form.get('city')
    house.house_type = request.form.get('house-type')
    house.pet_friendly = request.form.get('pet-friendly') == 'on'
    db.commit()
    db.close()
    return redirect(url_for('main'))
    
def delete_house(id):
    db = Config.SESSION()
    house = db.query(House).get(id)
    db.delete(house)
    db.commit()
    db.close()

    return redirect(url_for('main'))


def update_job_page(id):
    if UserId.get_user_id() == -1:
        return redirect(url_for('main'))
    db = Config.SESSION()
    job = db.query(Job).get(id)
    db.close()
    return render_template('updateJob.html', job=job, id=job.id)

def update_job(id):
    db = Config.SESSION()
    job = db.query(Job).get(id)
    job.city = request.form.get('city')
    job.name = request.form.get('name')
    job.description = request.form.get('description')
    job.sallary = int(request.form.get('sallary'))
    db.commit()
    db.close()
    return redirect(url_for('main'))
    
def delete_job(id):
    db = Config.SESSION()
    job = db.query(Job).get(id)
    db.delete(job)
    db.commit()
    db.close()

    return redirect(url_for('main'))