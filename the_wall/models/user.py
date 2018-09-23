from flask import request, session, request
from flask_bcrypt import Bcrypt

from the_wall import app
from the_wall.config.mysqlconnection import connectToMySQL

bcrypt = Bcrypt(app)
db_name = 'the_wall'

class User:
    def logInUser(self, way=''):
        if way:
            user = self.getUserById(way)
        else:
            user = self.getUserByEmail()

        if user and bcrypt.check_password_hash(user[0]['password'], request.form['password']):
            session['user_id'] = user[0]['id']
            session['user_first_name'] = user[0]['first_name']
            session['user_hash'] = bcrypt.generate_password_hash(str(user[0]['created_at']) + 'justDontBruh')
            session['logged_in'] = True
            session['showLoginModal'] = False
        return user

    def registerUser(self):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        query  = 'INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) '
        query += 'VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());'
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash,
        }
        mysql = connectToMySQL(db_name)
        newId = mysql.query_db(query, data)
        if newId:
            self.logInUser(newId)
        return newId

    def getUserByEmail(self):
        query = 'SELECT * from users WHERE email = %(email)s'
        data = {
            'email': request.form['email'],
        }
        mysql = connectToMySQL(db_name)
        return mysql.query_db(query, data)

    def getUserById(self, id):
        query = 'SELECT * from users WHERE id = %(id)s'
        data = {
            'id': id,
        }
        mysql = connectToMySQL(db_name)
        return mysql.query_db(query, data)
