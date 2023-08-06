from mongoengine import *

class AccessToken(Document):
    access = StringField(required=True)
    refresh = StringField(required=True)
    insert_date = DateTimeField(required=True)

