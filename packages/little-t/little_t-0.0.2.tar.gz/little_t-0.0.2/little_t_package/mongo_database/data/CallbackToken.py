from mongoengine import *

class CallbackToken(Document):
    code = StringField(required=True) 
    state = StringField(required=True) 
    insert_date = DateTimeField(required=True)

