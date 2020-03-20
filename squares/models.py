from datetime import datetime
from squares import db, login_manager
from flask_login import UserMixin
from flask import url_for


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


# class Item(db.Model):
#     pass

#     id = db.Column(db.Integer, primary_key=True)
#     manufacturer = db.Column(db.String(32), nullable=False)
#     catalog_no = db.Column(db.String(64), nullable=False)
#     image_url = db.Column(db.String(256), nullable=False)

#     def __repr__(self):
#         return f"Item('\n...{self.make}'\n\t '{self.model}' \n\t '{self.year}')"


class ItemDemo():
  pass
  base_url = 'https://shop.flexfit.com/product/image/medium/'

  def __init__(self, id='9999', manufacturer='YUUPONG',
               catalog_no='999DEMO', catalog_desc='noItemDesc',
               image_url=''
               ):
      pass
      self.id = id
      self.manufacturer = manufacturer
      self.image_url = image_url
      self.catalog_no = catalog_no
      self.catalog_desc = catalog_desc

  def __repr__(self):
      return f"Item('\n...{self.manufacturer}'\n\t '{self.catalog_no}')"
