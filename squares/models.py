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


class ItemDemo():
  pass

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
      return f"Item('\n...{self.manufacturer}'\n\t '{self.catalog_no}'\n\t '{self.image_url}')"


class Item(db.Model):
    pass
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(32))
    catalog_no = db.Column(db.String(32))
    catalog_fullname = db.Column(db.String(256))
    imagewhtbg_url = db.Column(db.String(256))
    imageclean_url = db.Column(db.String(256))
    color_primary = db.Column(db.String(32))
    color_secondary = db.Column(db.String(32))
    product_url = db.Column(db.String(256))
    inv_lowinstock = db.Column(db.String(32))
    inv_outofstock = db.Column(db.String(32))
    is_adjustable = db.Column(db.String(32))
    is_snapback = db.Column(db.String(32))
    is_flexfit = db.Column(db.String(32))
    is_fitted = db.Column(db.String(32))
    is_youth = db.Column(db.String(32))
    has_structcrwn = db.Column(db.String(32))
    has_curvedbill = db.Column(db.String(32))
    has_flatbill = db.Column(db.String(32))

    def display_properties(self):
        '''GENERATES A DICT OF ITEM PHYSICAL PROPERTIES FOR EASE OF FRONT END DESIGN'''
        pass
        labels = [
            'Snap Back',
            'Adjustable', 
            'FlexFit', 
            'Youth', 
            'Fitted', 
            'Structured',
            'Curved Bill',
            'Flat Bill',
        ]
        properties = [
            self.is_snapback, 
            self.is_adjustable,
            self.is_flexfit, 
            self.is_youth, 
            self.is_fitted, 
            self.has_structcrwn, 
            self.has_curvedbill, 
            self.has_flatbill,
        ]
        return dict(zip(labels, properties))

    def __repr__(self):
        return f"Item('\n...{self.manufacturer}'\n\t '{self.catalog_no}')"

