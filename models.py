# coding: UTF-8
from google.appengine.ext import db

class User(db.Model):
    name = db.StringProperty()

class InstaData(db.Model):
    instagram_id = db.IntegerProperty()
    url = db.StringProperty()
    image_url = db.StringProperty()
    content_type = db.StringProperty()
    thumbnail = db.BlobProperty()
    created_at = db.DateTimeProperty()
    twitter_name = db.StringProperty()
    twitter_message = db.StringProperty(multiline=True)
    twitter_url = db.StringProperty()

class SinceData(db.Model):
    since_id = db.IntegerProperty()

