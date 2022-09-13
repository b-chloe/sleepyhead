from flask_app.config.mysqlconnection import connectToMySQL
from .technique import Technique
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'sleepyhead'
    def __init__(self, data):
        self.id = data['id']
        self.fname = data['fname']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.techniques=[]

    @classmethod
    def create_user(cls, data):
        query="INSERT INTO users (fname, email, password, created_at, updated_at) VALUES (%(fname)s, %(email)s, %(password)s, NOW(), NOW());"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return results

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >= 1:
            print("HERE IS THE EMAIL====>",results)
            is_valid = False
            flash("Email is already in use")
        if len(user['fname']) < 2:
            is_valid = False
            flash("Names must be 2+ characters")
        if len(user['password']) < 6:
            is_valid = False
            flash("Passwords must have at least 6 characters")
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash("Invalid email address!")
        if user['password'] != user['confirm']:
            is_valid = False
            flash("Passwords don't match! Try again.")
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query='SELECT * FROM users where email = %(email)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        print("these are results of getting by email =====>", results)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def one_user(cls, data):
        query = 'SELECT * FROM users where id=%(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        # if len(results) < 1:
        #     return False
        # return cls(results[0])
        return results

    @classmethod
    def posted_by_user(cls, data):
        query = 'SELECT * FROM users LEFT JOIN techniques on users.id = techniques.users_id WHERE users.id = %(user_id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        print ("THESE ARE THE RESULTS ====>",results)
        users_posts = cls(results[0])
        for row in results:
            data = {
                'id':row['id'],
                'name': row['name'],
                'type': row['type'],
                'comments': row['comments'],
                'rating': row['rating'],
                'created_at':row['created_at'],
                'updated_at':row['updated_at'],
                'users_id':row['users_id']
            }
            users_posts.techniques.append(User(data))
        return(users_posts)