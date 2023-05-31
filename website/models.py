from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin): # Model = Table
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    tasks = db.relationship('Task', backref='user', passive_deletes=True) # if you want to get info inside user class do task.user.... If do task.author you get only id
    # comments = db.relationship('Comment', backref='user', passive_deletes=True)
    # likes = db.relationship('Like', backref='user', passive_deletes=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False) # user is adobted for SQL class User. It is not just some variable name
    date_deadline = db.Column(db.String(150))
    # users_task = db.relationship('User', backref='users_task', passive_deletes=True)
    # comments = db.relationship('Comment', backref='post', passive_deletes=True)
    # likes = db.relationship('Like', backref='post', passive_deletes=True)


# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(200), nullable=False)
#     date_created = db.Column(db.DateTime(timezone=True), default=func.now())
#     author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)

# class Like(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date_created = db.Column(db.DateTime(timezone=True), default=func.now())
#     author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)
