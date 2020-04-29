from django.db import models
from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel

connect('mongodb://localhost:27017/myApp')

# Create your models here.
class User(MongoModel):
    # Use 'email' as the '_id' field in MongoDB.
    email = fields.EmailField(primary_key=True)
    fname = fields.CharField()
    lname = fields.CharField()

class BlogPost(MongoModel):
    # This field references the User model above.
    # It's stored as a bson.objectid.ObjectId in MongoDB.
    author = fields.ReferenceField(User)
    title = fields.CharField(max_length=100)
    content = fields.CharField()
    tags = fields.ListField(fields.CharField(max_length=20))
    # These Comment objects will be stored inside each Post document in the
    # database.
    comments = fields.EmbeddedDocumentListField('Comment')

    class Meta:
        # Text index on content can be used for text search.
        indexes = [IndexModel([('content', TEXT)])]

# This is an "embedded" model and will be stored as a sub-document.
class Comment(EmbeddedMongoModel):
    author = fields.ReferenceField(User)
    body = fields.CharField()
    vote_score = fields.IntegerField(min_value=0)


class Tutorial(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200,blank=False, default='')
    published = models.BooleanField(default=False)