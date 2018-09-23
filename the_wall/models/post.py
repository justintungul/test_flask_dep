from flask import request, session, request
from flask_bcrypt import Bcrypt

from the_wall import app
from the_wall.config.mysqlconnection import connectToMySQL

import pprint
import datetime

bcrypt = Bcrypt(app)
db_name = 'the_wall'
pp = pprint.PrettyPrinter(indent=4)

class Post:
    def insertMessage(self):
        query  = 'INSERT INTO messages (user_id, message, created_at, updated_at) '
        query += 'VALUES (%(user_id)s, %(message)s, NOW(), NOW())'
        data = {
            'user_id': session['user_id'],
            'message': request.form['message']
        }
        mysql = connectToMySQL(db_name)
        newId = mysql.query_db(query, data)
        return newId

    def insertComment(self):
        query  = 'INSERT INTO comments (user_id, message_id, comment, created_at, updated_at) '
        query += 'VALUES (%(user_id)s, %(message_id)s, %(comment)s, NOW(), NOW())'
        data = {
            'user_id': session['user_id'],
            'message_id': request.form['message_id'],
            'comment': request.form['comment']
        }
        mysql = connectToMySQL(db_name)
        newId = mysql.query_db(query, data)
        return newId
    
    # def getAllPosts(self):
    #     query  = 'SELECT u2.first_name, u2.last_name, messages.id, message, messages.created_at, u1.first_name, u1.last_name, comments.id, comment, comments.created_at '
    #     query += 'FROM messages '
    #     query += 'JOIN comments ON messages.id = comments.message_id '
    #     query += 'JOIN users AS u1 ON comments.user_id = u1.id '
    #     query += 'JOIN users AS u2 ON messages.user_id = u2.id'

    #     mysql = connectToMySQL(db_name)
    #     posts = mysql.query_db(query)
        
    #     obj = []
    #     for objs in posts:
    #         for key, val in objs.items():
    #             temp = {
    #                 'id': 
    #             }

    #     print('-'*30, posts)
    #     return True

    def getAllPosts(self):
        query = 'SELECT * FROM messages JOIN users ON messages.user_id = users.id ORDER BY messages.created_at DESC'
        mysql = connectToMySQL(db_name)
        messages = mysql.query_db(query)

        query = 'SELECT * FROM comments JOIN users ON comments.user_id = users.id'
        mysql = connectToMySQL(db_name)
        comments = mysql.query_db(query)

        for msg in messages:
            msg['comments'] = []
            msg['date'] = self.datefy(msg['created_at'])

        for msg in messages:
            for com in comments:
                if msg['id'] == com['message_id']:
                    com['date'] = self.datefy(com['created_at'])
                    msg['comments'].append(com)

        # pp.pprint(messages)
        return messages

    def deleteMessageById(self, id, created_at):
        query = 'DELETE FROM messages WHERE id = %(message_id)s'
        data = {
            'message_id': id
        }
        now = datetime.datetime.now()
        created_at = datetime.datetime.strptime(created_at, '%Y-%m-%d %X')
        diff = now - created_at
        minutes = int(diff.total_seconds() / 60)
        print('-'*30, 'diff:', minutes)
        if minutes > 30:
            return False
        else:
            mysql = connectToMySQL(db_name)
            msg = mysql.query_db(query, data)
            return True

    def deleteCommentById(self, id, created_at):
        query = 'DELETE FROM comments WHERE id = %(comment_id)s'
        data = {
            'comment_id': id
        }
        now = datetime.datetime.now()
        created_at = datetime.datetime.strptime(created_at, '%Y-%m-%d %X')
        diff = now - created_at
        minutes = int(diff.total_seconds() / 60)
        print('-'*30, 'diff:', minutes)
        if minutes > 30:
            return False
        else:
            mysql = connectToMySQL(db_name)
            msg = mysql.query_db(query, data)
            return True

    def datefy(self, rawDate):
        date = rawDate
        month = date.strftime('%B')
        day = date.strftime('%d')
        rest = date.strftime('%Y %I:%M %p')
        if int(day[len(day) - 2: len(day)]) >= 11 and int(day[len(day) - 2: len(day)]) <= 13:
            day += 'th'
        elif day[len(day) - 1] == '1':
            day += 'st'
        elif day[len(day) - 1] == '2':
            day += 'nd'
        elif day[len(day) - 1] == '3':
            day += 'rd'
        else:
            day += 'th'

        if day[0] == '0':
            day = day[1:]
        
        dateFormat = month + ' ' + day + ', ' + rest
        return dateFormat



