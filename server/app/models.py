from flask_login import UserMixin
from app import mongo
from datetime import datetime

class User(UserMixin):
    def __init__(self, user_id, name, email , profile_pic):
        self.id = user_id
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        """ Fetch user from MongoDB """
        user = mongo.db.users.find_one({"_id": user_id})
        if user:
            return User(user["_id"], user["name"], user["email"] , user["profile_pic"])
        return None

    @staticmethod
    def create_or_update(user_id, name, email , profile_pic=None):
        """ Create new user if not exists, else update login time """
        user = mongo.db.users.find_one({"_id": user_id})

        if user:
            mongo.db.users.update_one(
                {"_id": user_id},
                {"$set": {"last_login": datetime.now() , "profile_pic": profile_pic}}
            )
        else:
            mongo.db.users.insert_one({
                "_id": user_id,
                "name": name,
                "email": email,
                "profile_pic": profile_pic,
                "created_at": datetime.now(),
                "last_login": datetime.now()
            })

        return User(user_id, name, email , profile_pic)
