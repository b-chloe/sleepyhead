from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Technique:
    db = 'sleepyhead'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.comments = data['comments']
        self.rating = data['rating']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.techniques=[]

    @classmethod
    def add_tip(cls, data):
        query="INSERT INTO techniques (name, type, comments, rating, created_at, updated_at, users_id) VALUES (%(name)s, %(type)s, %(comments)s, %(rating)s, NOW(), NOW(), %(user_id)s);"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return results

    # @classmethod
    # def update_tree(cls, data):
    #     query = 'UPDATE techniques SET species = %(species)s, Location = %(Location)s, reason = %(reason)s, date = %(date)s WHERE id_of_tree=%(id_of_tree)s;'
    #     return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all_tips(cls):
        query = 'SELECT * FROM techniques'
        results = connectToMySQL(cls.db).query_db(query)
        all_tips = []
        for one_tip in results:
            all_tips.append(cls(one_tip))
        print(all_tips)
        return all_tips

    @classmethod
    def posted_by_user(cls, data):
        query = 'SELECT * FROM users LEFT JOIN techniques on users.id = techniques.users_id WHERE users_id = %(user_id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        print ("THESE ARE THE RESULTS ====>",results)
        users_posts = cls(results[0])
        print("THESE ARE THE RESULTS!!!!", users_posts)
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
            users_posts.techniques.append(Technique(data))
        return(data)