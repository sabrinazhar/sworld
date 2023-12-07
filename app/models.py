# models.py

from datetime import datetime
from app import db
from flask_login import UserMixin

# Define followers table (Many-to-Many Relationship)
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

# Define post_followers table (Many-to-Many Relationship)
post_followers = db.Table('post_followers',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

# Define User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    font_size = db.Column(db.String(10), default='normal')
    
    # Define followers relationship
    followers = db.relationship('User', secondary='followers',
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('following', lazy='dynamic'), lazy='dynamic')

    def get_id(self):
        return str(self.id)

    def is_active(self):
        # You can customize this method based on your application's requirements
        return True

    def is_authenticated(self):
        # You can customize this method based on your application's requirements
        return True

    def is_anonymous(self):
        return False

# Define Post Model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    # Inside the Post class
    def has_user_liked(self, user):
        return Like.query.filter_by(post_id=self.id, user_id=user.id).first() is not None

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('likes', lazy=True))
    post = db.relationship('Post', backref=db.backref('likes', lazy=True))
