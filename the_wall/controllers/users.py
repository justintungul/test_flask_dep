from flask import redirect, render_template, session, request, flash
from the_wall.models.user import User
import re

user = User()
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NUMERICAL_REGEX = re.compile(r'^(0|[1-9][0-9]*)$')

class Users:
    def login(self):
        res = user.logInUser()
        print('-'*30, 'user:', res)

        if res:
            return redirect('/wall')
        else:
            flash('Unable to log-in', 'error')
            session['showLoginModal'] = True
            return redirect('/')

    def register(self):
        first_name, last_name, email, password, birthday = False, False, False, False, False

        if len(request.form['first_name']) < 2 or NUMERICAL_REGEX.match(request.form['first_name']) is not None:
            flash('First name should be at least 2 non-numberic characters', 'first_name')
            session['first_name'] = ''
        else:
            session['first_name'] = request.form['first_name']
            first_name = True

        if len(request.form['last_name']) < 2 or NUMERICAL_REGEX.match(request.form['last_name']) is not None:
            flash('Last name should be at least 2 non-numberic characters', 'last_name')
            session['last_name'] = ''
        else:
            session['last_name'] = request.form['last_name']
            last_name = True

        if len(request.form['email']) < 1:
            flash('Email cannot be blank', 'email')
            session['email'] = ''
        elif not EMAIL_REGEX.match(request.form['email']):
            flash("Please enter a valid email address", 'email')
        else:
            session['email'] = request.form['email']
            email = True

        if len(request.form['password']) < 1:
            flash('Password cannot be blank', 'password')
        elif len(request.form['password']) < 8:
            flash('Password should be at least 8 characters', 'password')
            session['password'] = ''
        elif request.form['password'] != request.form['confirm']:
            flash('Passwords do not match', 'confirm')
            session['password'] = ''
            session['confirm'] = ''
        else:
            session['password'] = request.form['password']
            password = True

        if first_name and last_name and email and password:
            newId = user.registerUser()
            print('-'*30, 'userId:', newId)
            return redirect('/wall')
        else:
            return redirect('/')

    def logout(self):
        session.clear()
        return redirect('/')