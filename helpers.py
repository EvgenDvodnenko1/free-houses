from flask import render_template, redirect, url_for
from models import Config

class UserId:
    id = -1

    @classmethod
    def get_user_id(cls):
        return cls.id
    
    @classmethod
    def set_user_id(cls, new_id):
        cls.id = new_id
        print(f'set id {new_id}')


def check_form(request, dependencies):
    for i in range(len(dependencies)):
        if not request.form.get(dependencies[i]):
            return render_template('error.html', error_text='All form fields should be provided')
        
    return True


def error_page(error_text):
    return render_template('error.html', error_text=error_text)

def check_id():
    if UserId.get_user_id() == -1:
        return redirect(url_for('main'))