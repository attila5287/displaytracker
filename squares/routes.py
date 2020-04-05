from collections import defaultdict
import random
import os
import secrets
import csv
import codecs
from PIL import (
    Image
)
from flask import (
    render_template, url_for, flash, redirect, request, abort, jsonify
)
from squares import (
    app, db, bcrypt
)
from squares.forms import (
    RegistrationForm, LoginForm,
    UpdateAccountForm, PostForm, ItemForm,
    CSVReaderForm, SquareForm, Form
)
from squares.models import (
    User, Post, Item, Square, Unit
)
from flask_login import (
    login_user, current_user, logout_user, login_required
)


@app.route("/item/<int:item_id>/delete", methods=['GET', 'POST'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item has been deleted from inventory!', 'danger')
    return redirect(url_for('inv_lister'))


# updateitem
@app.route("/item/<int:item_id>/edit", methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    # trick is the obj to show item info on the form
    form = ItemForm(obj=item)
    if form.validate_on_submit():
        pass
        item.update_via_wtforms(form)
        db.session.commit()
        flash('Item Updated!', 'success')
        return redirect(url_for('show_item', item_id=item_id))

    return render_template(
        'edit_item.html',
        item=item,
        form=form,
        title='Edit Item',
        legend='Edit Form For Item ID: '+str(item.id)
    )


@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = Item.query.get_or_404(item_id)
    custom_title = 'Show ' + str(item.id) + ' ' + item.catalog_fullname
    return render_template('show_item.html', title=custom_title, legend='Show Item ' + str(item.id), item=item)

# @app.route("/")


@app.route("/inventory/list")
def inv_lister():
    pass
    page = request.args.get('page', 1, type=int)
    inventory = Item.query.order_by(
        Item.id.desc()).paginate(page=page, per_page=10)

    return render_template(
        'inv_lister.html',
        inventory=inventory,
        title='InvListMaster'
    )


@app.route("/markas/outofstock/<int:item_id>")
def mark_as_outofstock(item_id):
    pass

    def redir3ct_url(default='inv_lister'):
        pass
        return request.referrer or \
            request.args.get('next') or \
            url_for(default)
    item = Item.query.get(item_id)  # this is the item to edit
    print()
    print(item)

    if item.inv_outofstock == 'no':
        pass
        item.just_ran_out()
        db.session.commit()
    elif item.inv_outofstock == 'yes':
        pass
        item.now_restock3d()
        db.session.commit()
    else:
        pass
        print('\n\t item could not be modified check yes-no values')

    return redirect(redir3ct_url())


@app.route("/markas/lowinv/<int:item_id>")
def mark_as_lowinv(item_id):
    pass

    def redir3ct_url(default='inv_lister'):
        pass
        return request.referrer or \
            request.args.get('next') or \
            url_for(default)
    print('item to edit is....')
    item = Item.query.get(item_id)
    print(item)

    if item.inv_lowinstock == 'no':
        pass
        item.running_low()
        db.session.commit()
    elif item.inv_lowinstock == 'yes':
        pass
        item.now_restocked()
        db.session.commit()
    else:
        pass
        print('\n\t item could not be modified check yes-no values')

    return redirect(redir3ct_url())


# inv_feed (doc: CSV read ex)
@app.route('/inventory/feed', methods=['GET', 'POST'])
def csv_feed():
    form = CSVReaderForm()
    if request.method == 'POST':
        csvfile = request.files['csv_file']
        reader = csv.DictReader(codecs.iterdecode(csvfile, 'windows-1252'))
        inventory = [
            Item(**row) for row in reader
        ]

        db.session.add_all(inventory)
        db.session.commit()

        flash('CSV read successfully!', 'success')
        return render_template('inv_home.html', inventory=inventory)

    return render_template(
        'csv_feed.html',
        title='CSV Feed',
        form=form,
    )


@app.route("/inventory/home")
def inv_home():
    pass

    inventory = Item.query.all()

    try:
        _ = [item for item in inventory]
    except:
        inventory = []

    return render_template('inv_home.html', inventory=inventory, title='InvDemoRandCol')


@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/inventory/new", methods=['GET', 'POST'])
@login_required
def create_item():
    form = ItemForm()
    if form.validate_on_submit():
        dict_userInput = dict(request.form)
        dict_userInput.pop('csrf_token')
        # this trick removes seventeen lines of code
        # thx to python dictionary
        # (resources>userInputDictTrick.txt)
        item = Item(**dict_userInput)
        db.session.add(item)
        db.session.commit()
        flash('Item added to inventory!', 'success')
        return redirect(url_for('inv_home'))

    return render_template('create_item.html', title='New Item',
                           form=form, legend='New Item')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# updatepost
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.context_processor
def inject_TableHeaders():
    ''' GENERATES A LIST OF ITEM ATTRIBUTES TO BE USED AS TABLE HEADERS '''
    pass
    _list = [
        "Snapback",
        "Adjustable",
        "Flexfit",
        "Youth",
        "Fitted",
        "Structured",
        "CurvedBill",
        "FlatBill",
    ]
    DisplayHeaders = [header for header in _list]
    return dict(DisplayHeaders=DisplayHeaders)


@app.context_processor
def inject_LowInvButtons():
    pass

    def LowInStckStyler(yes_or_no):
        '''DICTIONARY CONTAINS BUTTON STYLES FOR LOW-INV '''
        pass
        _btnStylesDict = {
            'yes': 'btn-warning btn-lg py-2 px-5',
            'no': 'btn-outline-secondary py-2 px-5',
        }
        return _btnStylesDict.get(yes_or_no, 'btn-outline-warning')
    return dict(LowInStckStyler=LowInStckStyler)


@app.context_processor
def inject_UnitInvOutStyler():
    pass

    def UnitInvOutStyler(yes_or_no):
        '''DICTIONARY CONTAINS BUTTON STYLES FOR LOW-INV '''
        pass
        _borderStylesDict = {
            'yes': 'primary',
            'no': '0',
        }
        return _borderStylesDict.get(yes_or_no, 'dark')
    return dict(UnitInvOutStyler=UnitInvOutStyler)


@app.context_processor
def inject_UnitInvOutIconizer():
    pass

    def UnitInvOutIconizer(yes_or_no):
        '''DICTIONARY CONTAINS BUTTON STYLES FOR LOW-INV '''
        pass
        _iconYesNoDict = {
            'no': 'check text-success',
            'yes': 'times text-primary ml-1',
        }
        return _iconYesNoDict.get(yes_or_no, 'question-circle')
    return dict(UnitInvOutIconizer=UnitInvOutIconizer)


@app.context_processor
def inject_OutInvButtons():
    pass

    def OutOfStckStyler(yes_or_no):
        '''DICTIONARY CONTAINS BUTTON STYLES FOR LOW-INV '''
        pass
        _btnStylesDict = {
            'yes': 'btn-danger btn-lg py-2 px-5',
            'no': 'btn-outline-secondary py-2 px-5',
        }
        return _btnStylesDict.get(yes_or_no, 'btn-outline-danger p-3')
    return dict(OutOfStckStyler=OutOfStckStyler)


@app.context_processor
def inject_OutInvBtns4Grid():
    pass

    def OutOfStckStylerGrid(yes_or_no):
        '''DICTIONARY CONTAINS BUTTON STYLES FOR LOW-INV '''
        pass
        _btnStylesDict = {
            'yes': 'btn-warning btn-md',
            'no': 'btn-outline-secondary',
        }
        return _btnStylesDict.get(yes_or_no, 'btn-outline-danger p-3')
    return dict(OutOfStckStylerGrid=OutOfStckStylerGrid)


@app.context_processor
def inject_LowInvBts4Grid():
    pass

    def LowInStckStylerGrid(yes_or_no):
        '''DICTIONARY CONTAINS BUTTON STYLES FOR LOW-INV '''
        pass
        _btnStylesDict = {
            'yes': 'btn-primary btn-md',
            'no': 'btn-outline-secondary',
        }
        return _btnStylesDict.get(yes_or_no, 'btn-outline-warning')
    return dict(LowInStckStylerGrid=LowInStckStylerGrid)


@app.context_processor
def inject_YesNoIcons():
    pass

    def YesNoIconizer(yes_or_no):
        '''DICTIONARY CONTAINS FONT AWESOME ICONS'''
        pass
        _iconYesNoDict = {
            'no': 'fa-times text-dark',
            'yes': 'fa-check',
        }
        return _iconYesNoDict.get(yes_or_no, 'fa-square fa-2x')
    return dict(YesNoIconizer=YesNoIconizer)


@app.context_processor
def inject_LowInvIcons():
    pass

    def LowInvIconizer(yes_or_no):
        '''DICTIONARY CONTAINS FONT AWESOME ICONS FOR LOW-INV '''
        pass
        _iconYesNoDict = {
            'no': 'fa-thumbs-up',
            'yes': 'fa-sort-amount-down text-light',
        }
        return _iconYesNoDict.get(yes_or_no, 'fa-square')
    return dict(LowInvIconizer=LowInvIconizer)


@app.context_processor
def inject_OutInvIcons():
    pass

    def OutInvIconizer(yes_or_no):
        '''DICTIONARY CONTAINS FONT AWESOME ICONS FOR OUT-INV '''
        pass
        _iconYesNoDict = {
            'no': 'fa-thumbs-up',
            'yes': 'fa-battery-empty text-light',
        }
        return _iconYesNoDict.get(yes_or_no, 'fa-square')
    return dict(OutInvIconizer=OutInvIconizer)


@app.route("/filterby/manuf/<string:item_manufacturer>")
def filterby_manuf(item_manufacturer):
    pass
    inventory = Item.query.filter_by(manufacturer=item_manufacturer).all()

    try:
        _ = [item for item in inventory]
    except:
        inventory = []
    return render_template(
        'inv_lister.html',
        inventory=inventory,
        title='InvFilterByManuf'
    )


@app.route("/showonly/lowinstock/yes")
def showonly_invlow():
    pass
    page = request.args.get('page', 1, type=int)
    inventory = Item.query.filter_by(inv_lowinstock='yes').order_by(
        Item.id.desc()).paginate(page=page, per_page=10)

    return render_template(
        'inv_lister.html',
        inventory=inventory,
        title='InvShowOnlyLow'
    )


@app.route("/showonly/outofstock/yes")
def showonly_invout():
    pass
    page = request.args.get('page', 1, type=int)
    inventory = Item.query.filter_by(inv_outofstock='yes').order_by(
        Item.id.desc()).paginate(page=page, per_page=10)

    return render_template(
        'inv_lister.html',
        inventory=inventory,
        title='InvShowOnlyOut'
    )


@app.route('/createall/squares')
def createall_squares():
    pass
    _names = [
        'snapback1',
        'snapback2',
        'snapback3',
        'adjustable',
        'flexfit1',
        'flexfit2',
        'youth',
        'fitted1',
        'fitted2',
        'fitted3',
    ]

    squares = [
        Square(name=_name, row_count=9, col_count=6) for _name in _names
    ]
    db.session.add_all(squares)
    db.session.commit()
    flash('all squares created', 'info')
    return redirect(url_for('sqr_home'))


@app.route('/findnext/byid/<int:item_id>', methods=['GET', 'POST'])
def findnext_byid(item_id=10):
    '''FIND NEXT ITEM BY PULLING THE MAIN-ITEM BY ID AND QUERY BY ITS ATTR'''
    pass

    def redir3ct_url(default='inv_lister'):
        pass
        return request.referrer or \
            request.args.get('next') or \
            url_for(default)

    item = Item.query.get_or_404(item_id)

    print('\n {} \n test find next'.format(item))

    only_yes = item.similar_attrs()

    suggested_items = Item.query.filter_by(**only_yes).all()

    next_item = random.choice(suggested_items)

    print('\n next item is', next_item)

    return redirect(redir3ct_url())


@app.route('/<string:unique_tag>/findnext/byid/<int:item_id>', methods=['GET', 'POST'])
def unit_nextitem(unique_tag, item_id):
    '''FIND NEXT ITEM BY PULLING THE CURRENTT-ITEM BY ID AND QUERY BY ITS ATTR'''
    pass
    unit = Unit.query.filter_by(unique_tag=unique_tag).first()
    item = Item.query.get_or_404(item_id)

    print('\n {} \n test find next'.format(item))
    only_yes = item.similar_attrs()
    suggested_items = Item.query.filter_by(**only_yes).all()
    next_item = random.choice(suggested_items)
    print('\n unit next item is\n', next_item)

    unit.dispitem_id = next_item.id
    db.session.commit()

    return redirect(url_for('square_byid', square_id=unit.square_id))


@app.route('/unit/<string:unique_tag>/update/mainitem/invout')
def unit_update_maininvout(unique_tag):
    pass
    unit = Unit.query.filter_by(unique_tag=unique_tag).first()
    item = Item.query.get_or_404(unit.mainitem_id)
    unit.maininv_out = item.inv_outofstock
    db.session.commit()
    return redirect(url_for('square_byid', square_id=unit.square_id))


@app.route('/unit/<string:unique_tag>/show/mainitem')
def unit_show_mainitem(unique_tag):
    pass
    unit = Unit.query.filter_by(unique_tag=unique_tag).first()
    item = Item.query.get_or_404(unit.mainitem_id)
    unit.dispitem_id = unit.mainitem_id
    unit.maininv_out = item.inv_outofstock
    db.session.commit()
    return redirect(url_for('square_byid', square_id=unit.square_id))


@app.route('/fixall/uniquetags/in/1', methods=['GET', 'POST'])
def fixall_uniquetags_in():
    pass
    units = Unit.query.filter_by(square_id=1).all()
    for unit in units:
        pass
        unit.unique_tag = 'S'+str(1)+'_'+unit.pstn_rowcol
        db.session.commit()
    flash('all unique tags fixed', 'danger')

    return redirect(url_for('sqr_home'))


@app.route('/fixfirst/units/mainitem')
def fixfirst_units_main():
    pass
    units = Unit.query.filter_by(square_id=1).all()
    for unit in units:
        pass
        _int = unit.dispitem_id
        unit.mainitem_id = _int
        db.session.commit()
    flash('all units main item ids fixed', 'warning')
    return redirect(url_for('sqr_home'))


@app.route('/createfirst/units')
def createfirst_units():
    pass
    items = Item.query.all()
    list_of_ids = [
        _item.id for _item in items
    ]
    _rows = [
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        'H',
        'I',
    ]
    _cols = [
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
    ]
    _rowcols = [
        row+column for row in _rows for column in _cols
    ]
    _tags = [
        'S1_'+_position for _position in _rowcols
    ]
    random.seed(42)
    units = [
        Unit(
            square_id=1,
            pstn_rowcol=_position,
            unique_tag=_tag,
            mainitem_id=1,
            maininv_out='no',
            dispitem_id=random.choice(list_of_ids),
        ) for _position, _tag in zip(_rowcols, _tags)
    ]
    db.session.add_all(units)
    db.session.commit()
    flash('all units created!', 'primary')
    return redirect(url_for('sqr_home'))


@app.route("/unit/update/invout")
def update_firstunits_invout():
    pass
    units = Unit.query.filter_by(square_id=1).all()

    for unit in units:
        pass
        item = Item.query.get_or_404(unit.mainitem_id)
        _updated_status = item.inv_outofstock
        unit.maininv_out = _updated_status
        db.session.commit()
    flash('all units main item inv status updated', 'info')

    return redirect(url_for('sqr_home'))


@app.route('/square/byid/<int:square_id>')
def square_byid(square_id):
    pass
    units = Unit.query.filter_by(square_id=square_id).\
        order_by(Unit.id.asc()).all()[:18]

    unit_unqtags = [
        unit.unique_tag for unit in units
    ]

    unit_dispitem_ids = [
        unit.dispitem_id for unit in units
    ]
    unit_itemid = dict(zip(units, unit_dispitem_ids))
    unqtag_itemid = dict(zip(unit_unqtags, unit_dispitem_ids))
    result_items = Item.query.filter(Item.id.in_(unit_dispitem_ids)).all()

    result_itemids = [
        item.id for item in result_items
    ]
    results_itemid_dict = dict(zip(result_itemids, result_items))
    display = dict()
    print('\ndisplay: ', display)
    for unit, query_untdispid in unit_itemid.items():
        pass

        for result_itemid, result_item in results_itemid_dict.items():
            pass

            if int(query_untdispid) == int(result_itemid):
                pass
                display[unit] = result_item

    print('\n display final')
    print(display)

    return render_template(
        'square_00.html',
        display=display,
        title='ShowSquareID: '+str(square_id),
    )


@app.route('/square/byid/<int:square_id>/lite')
def square_byid_lite(square_id):
    pass
    units = Unit.query.filter_by(square_id=square_id).\
        order_by(Unit.id.asc()).all()

    unit_unqtags = [
        unit.unique_tag for unit in units
    ]

    unit_dispitem_ids = [
        unit.dispitem_id for unit in units
    ]
    unit_itemid = dict(zip(units, unit_dispitem_ids))
    unqtag_itemid = dict(zip(unit_unqtags, unit_dispitem_ids))
    result_items = Item.query.filter(Item.id.in_(unit_dispitem_ids)).all()

    result_itemids = [
        item.id for item in result_items
    ]
    results_itemid_dict = dict(zip(result_itemids, result_items))
    display = dict()
    print('\ndisplay: ', display)
    for unit, query_untdispid in unit_itemid.items():
        pass

        for result_itemid, result_item in results_itemid_dict.items():
            pass

            if int(query_untdispid) == int(result_itemid):
                pass
                display[unit] = result_item

    print('\n display final')
    print(display)

    return render_template(
        'square_00_lite.html',
        display=display,
        title='ShowSquareID: '+str(square_id),
    )


# squares_all
@app.route('/squares/all', methods=['GET', 'POST'])
def sqr_home():
    ''' SQUARE-HOME: ALL SQRS'''
    pass
    form = SquareForm()
    form.opts.query = Square.query.all()
    squares = Square.query.all()

    if request.method == 'POST':
        pass
        # request form returns id as int thx-to square_query func in app.forms
        userselection = request.form['opts']
        return redirect(url_for('square_byid', square_id=userselection))

    return render_template(
        'squares_home.html',
        form=form,
        squares=squares,
        title='SqrHome',
    )


@app.route('/color/finder', methods=['GET', 'POST'])
def color_finder():
    items = Item.query.all()

    primary_colors = [
        item.color_primary for item in items
    ]

    secondary_colors = [
        item.color_secondary for item in items
    ]

    all_colors = primary_colors + secondary_colors
    print(all_colors)

    d = defaultdict(int)
    for color in all_colors:
        d[color] += 1

    for color, count in d.items():
        pass
        print(color)

    return redirect(url_for('sqr_home'))


@app.route("/unit/<string:unique_tag>/markas/mainlow/<int:item_id>")
def unit_mainitem_low(unique_tag, item_id):
    pass

    def redir3ct_url(default='inv_lister'):
        pass
        return request.referrer or \
            request.args.get('next') or \
            url_for(default)

    item = Item.query.get(item_id)
    unit = Unit.query.filter_by(unique_tag=unique_tag).first()

    if item.inv_lowinstock == 'no':
        pass
        item.running_low()
        unit.mainitem_restck()

        db.session.commit()
    elif item.inv_lowinstock == 'yes':
        pass
        unit.mainitem_restck()
        item.now_restocked()
        db.session.commit()
    else:
        pass
        print('\n\t unit or item could not be modified check again')

    return redirect(redir3ct_url())


@app.route("/unit/<string:unique_tag>/markas/mainout/<int:item_id>")
def unit_mainitem_out(unique_tag, item_id):
    pass

    def redir3ct_url(default='sqr_home'):
        pass
        return request.referrer or \
            request.args.get('next') or \
            url_for(default)
    item = Item.query.get(item_id)
    unit = Unit.query.filter_by(unique_tag=unique_tag).first()

    if item.inv_outofstock == 'no':
        pass
        item.just_ran_out()
        unit.maininv_out = 'yes'
        db.session.commit()
    elif item.inv_outofstock == 'yes':
        pass
        item.now_restock3d()
        unit.maininv_out = 'no'
        db.session.commit()
    else:
        pass
        print('\n\t item could not be modified check yes-no values')

    return redirect(redir3ct_url())


# ------------dynamic-JS------------
@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    form.item.choices = [
        (item.id, \
            item.catalog_no + ' ' + item.color_primary + ' ' + item.color_secondary)
            for item in Item.query.filter_by(manufacturer='OTTO').all()
            ]

    if request.method == 'POST':
        item = Item.query.filter_by(id=form.item.data).first()
        return '<h1>Manufacturer: {}, Catalog No: {}</h1>'.format(form.manufacturer.data, item.catalog_no)

    return render_template('index.html', form=form)


@app.route('/manufacturer/<string:manufacturer>', methods=['GET', 'POST'])
def fetchitems_by(manufacturer):
    q_items = Item.query.filter_by(manufacturer=manufacturer).all()

    itemArray = [
        {
            'id': item.id,
            'catalog_no': item.catalog_no,
            'color_primary': item.color_primary,
            'color_secondary': item.color_secondary
        }
        for item in q_items
    ]

    return jsonify({'items': itemArray})


@app.route('/fetch/ddslick/<string:manufacturer>', methods=['GET', 'POST'])
def fetch_ddslick(manufacturer):
    q_items = Item.query.filter_by(manufacturer=manufacturer).all()

    img_baseURL = 'https://raw.githubusercontent.com/attila5287/displayTracker_img/master/img/list/'

    itemArray = [
        {
            'text': item.catalog_no,
            'value': item.id,
            'selected': False,
            'description': item.color_primary+' '+item.color_secondary,
            'imageSrc': img_baseURL+item.manufacturer+'/'+item.imagelist_url
        }
        for item in q_items
    ]

    return jsonify({'ddData': itemArray})


@app.route('/ddslick/demo', methods=['GET', 'POST'])
def ddslick_demo():
    pass

    return render_template('ddslick_demo.html')

@app.route('/ddslick/master', methods=['GET', 'POST'])
def ddslick_master():
    pass

    return render_template('ddslick_master.html')


if __name__ == '__main__':
    app.run(debug=True)
