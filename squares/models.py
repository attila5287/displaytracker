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
    catalog_fullname = db.Column(db.String(256))
    color_primary = db.Column(db.String(32))
    color_secondary = db.Column(db.String(32))
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
    imagewhtbg_url = db.Column(db.String(256))
    imageclean_url = db.Column(db.String(256))
    product_url = db.Column(db.String(256))

    __mapper_args__ = {
        'polymorphic_identity': 'item'
    }

    def __repr__(self):
        return f"Item('\n...{self.manufacturer}'\n\t '{self.catalog_fullname}')"

    def display_properties(self):
        '''GENERATES A DICT OF ITEM PHYSICAL PROPERTIES FOR EASE OF FRONT END DESIGN FOR INV-HOME'''
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

    def display_tablerow(self):
        '''GENERATES A LIST OF ITEM YES-NO ATTRIBUTES FOR EASE OF FRONT-END DESIGN INV-LISTER'''
        pass
        _tablerow_data = [
            self.is_snapback,
            self.is_adjustable,
            self.is_flexfit,
            self.is_youth,
            self.is_fitted,
            self.has_structcrwn,
            self.has_curvedbill,
            self.has_flatbill,
        ]
        return [td for td in _tablerow_data]
        
    def running_low(self):
        pass
        self.inv_lowinstock = 'yes'
        self.inv_outofstock = 'no'

    def now_restocked(self):
        pass
        self.inv_lowinstock = 'no'

    def just_ran_out(self):
        pass
        self.inv_lowinstock = 'no'
        self.inv_outofstock = 'yes'

    def now_restock3d(self):
        pass
        self.inv_outofstock = 'no'

    def gen_attr_dict(self):
        ''' GENERATE A DICT WITH ALL CLASS ATTR AND INSTNCE AS KEY-VALUE PAIRS '''
        pass
        _attrs = [
            'id',
            'manufacturer',
            'catalog_fullname',
            'color_primary',
            'color_secondary',
            'inv_lowinstock',
            'inv_outofstock',
            'is_snapback',
            'is_adjustable',
            'is_flexfit',
            'is_youth',
            'is_fitted',
            'has_structcrwn',
            'has_curvedbill',
            'has_flatbill',
            'imagewhtbg_url',
            'imageclean_url',
            'product_url',

        ]
        _values = [
            str(self.id),
            self.manufacturer,
            self.catalog_fullname,
            self.color_primary,
            self.color_secondary,
            self.inv_lowinstock,
            self.inv_outofstock,
            self.is_snapback,
            self.is_adjustable,
            self.is_flexfit,
            self.is_youth,
            self.is_fitted,
            self.has_structcrwn,
            self.has_curvedbill,
            self.has_flatbill,
            self.imagewhtbg_url,
            self.imageclean_url,
            self.product_url,
        ]
        return dict(zip(_attrs, _values))

    def update_via_wtforms(self, form):
        pass
        self.manufacturer = form.manufacturer.data
        self.catalog_fullname = form.catalog_fullname.data
        self.color_primary = form.color_primary.data
        self.color_secondary = form.color_secondary.data
        self.imagewhtbg_url = form.imagewhtbg_url.data
        self.imageclean_url = form.imageclean_url.data
        self.product_url = form.product_url.data
        self.inv_lowinstock = form.inv_lowinstock.data
        self.inv_outofstock = form.inv_outofstock.data
        self.is_snapback = form.is_snapback.data
        self.is_adjustable = form.is_adjustable.data
        self.is_flexfit = form.is_flexfit.data
        self.is_youth = form.is_youth.data
        self.is_fitted = form.is_fitted.data
        self.has_structcrwn = form.has_structcrwn.data
        self.has_curvedbill = form.has_curvedbill.data
        self.has_flatbill = form.has_flatbill.data
        print('\n\t... models.item no {}  u p d a t e d ...\n'.format(self.id))



class Square(db.Model):
    '''A SQUARE CONTAINS 6 ITEMS IN EA. ROW and 9 IN COL '''
    pass
    __tablename__ = 'square'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    row_count = db.Column(db.Integer)
    col_count = db.Column(db.Integer)

class Squar3(db.Model):
    '''A SQUARE CONTAINS 6 ITEMS IN EA. ROW and 9 IN COL '''
    pass
    __tablename__ = 'squar3'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    A1 = db.Column(db.Integer)
    A2 = db.Column(db.Integer)
    A3 = db.Column(db.Integer)
    A4 = db.Column(db.Integer)
    A5 = db.Column(db.Integer)
    A6 = db.Column(db.Integer)

    B1 = db.Column(db.Integer)
    B2 = db.Column(db.Integer)
    B3 = db.Column(db.Integer)
    B4 = db.Column(db.Integer)
    B5 = db.Column(db.Integer)
    B6 = db.Column(db.Integer)

    C1 = db.Column(db.Integer)
    C2 = db.Column(db.Integer)
    C3 = db.Column(db.Integer)
    C4 = db.Column(db.Integer)
    C5 = db.Column(db.Integer)
    C6 = db.Column(db.Integer)

    D1 = db.Column(db.Integer)
    D2 = db.Column(db.Integer)
    D3 = db.Column(db.Integer)
    D4 = db.Column(db.Integer)
    D5 = db.Column(db.Integer)
    D6 = db.Column(db.Integer)

    E1 = db.Column(db.Integer)
    E2 = db.Column(db.Integer)
    E3 = db.Column(db.Integer)
    E4 = db.Column(db.Integer)
    E5 = db.Column(db.Integer)
    E6 = db.Column(db.Integer)

    F1 = db.Column(db.Integer)
    F2 = db.Column(db.Integer)
    F3 = db.Column(db.Integer)
    F4 = db.Column(db.Integer)
    F5 = db.Column(db.Integer)
    F6 = db.Column(db.Integer)

    G1 = db.Column(db.Integer)
    G2 = db.Column(db.Integer)
    G3 = db.Column(db.Integer)
    G4 = db.Column(db.Integer)
    G5 = db.Column(db.Integer)
    G6 = db.Column(db.Integer)

    H1 = db.Column(db.Integer)
    H2 = db.Column(db.Integer)
    H3 = db.Column(db.Integer)
    H4 = db.Column(db.Integer)
    H5 = db.Column(db.Integer)
    H6 = db.Column(db.Integer)

    I1 = db.Column(db.Integer)
    I2 = db.Column(db.Integer)
    I3 = db.Column(db.Integer)
    I4 = db.Column(db.Integer)
    I5 = db.Column(db.Integer)
    I6 = db.Column(db.Integer)

class Unit(Item):
    '''EA. UNIT WILL SUGGEST MAIN-ALTERNATIVE-ITEMS OR 
    SET MANUALLY EA.SQUARE WILL HAVE 54 UNITS'''
    pass
    __tablename__ = 'unit'

    id = db.Column(db.Integer, primary_key=True)
    square_id = db.Column(db.Integer)
    pstn_rowcol = db.Column(db.String(32))
    unique_tag = db.Column(db.String(32))
    mainitem_id = db.Column(db.Integer)
    maininv_out = db.Column(db.String(32))
    dispitem_id = db.Column(
        db.Integer, db.ForeignKey('item.id')
        )


    def __repr__(self):
        pass
        square_id = str(self.square_id)
        position = self.pstn_rowcol
        margin = ''
        if square_id != '10':
            margin = ' '

        top = '\n┌───┐'
        square_id_left = '│s{}{}│'.format(square_id, margin)
        frame_lower = '│ {}│'.format(position)
        bottom = '└───┘'
        str_list = [
            # t1tle,
            # margin_top,
            top,
            square_id_left,
            frame_lower,
            bottom
        ]

        return '\n'.join(str_list)
