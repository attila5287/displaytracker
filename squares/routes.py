import random
import os
import secrets
import csv
import codecs
from PIL import (
    Image
)
from flask import (
    render_template, url_for, flash, redirect, request, abort,
)
from squares import (
    app, db, bcrypt
)
from squares.forms import (
    RegistrationForm, LoginForm, UpdateAccountForm, PostForm, ItemForm, CSVReaderForm
)
from squares.models import (
    User, Post, ItemDemo, Item, Squar3, Square, Unit
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
    custom_title = 'Show ' + str(item.id) + ' ' +  item.catalog_fullname
    return render_template('show_item.html', title=custom_title, legend='Show Item ' + str(item.id), item=item)


@app.route("/")
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


@app.route('/fixfirst/units')
def fixfirst_units():
    pass
    units = Unit.query.filter_by(square_id=1).all()
    for unit in units:
        pass
        _int = unit.mainitem_id
        unit.dispitem_id = _int
        db.session.commit()
    return redirect(url_for('about'))


@app.route('/createfirst/units')
def createfirst_units():
    pass
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
        's1'+_position for _position in _rowcols
    ]
    
    units = [
        Unit(
            square_id=1,
            pstn_rowcol=_position,
            unique_tag=_tag,
            mainitem_id=random.randint(1, 96),
            maininv_out='no',
            dispitem_id  =random.randint(1, 96),
        ) for _position, _tag in zip(_rowcols, _tags)
    ]
    db.session.add_all(units)
    db.session.commit()

    return redirect(url_for('about'))


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
    return redirect(url_for('square_00', square_id=1))

# old route now squar3
@app.route('/square/<int:square_id>')
def square_00(square_id):
    square = Squar3.query.filter_by(id=square_id).first()
    display = []
    seq = [
        _id for _id in range(33, 87)
    ]
    display = Item.query.filter(Item.id.in_(seq)).all()


    return render_template(
        'square_00.html',
        display=display,
        title=square.name.upper(),
    )


@app.route('/showbyid/square/<int:square_id>')
def showsqr_byid(square_id):
    pass

    units = Unit.query.filter_by(square_id=square_id).all()

    print(*units)

    displayed_item_ids = [
        unit.dispitem_id for unit in units
    ]
    seq = [
        _id for _id in displayed_item_ids
    ]
    print(seq)
    display = Item.query.filter(Item.id.in_(seq)).all()

    


     
    print(display)
    return render_template(
        'square_00.html',
        display=display,
        title='ShowSquareID: '+str(square_id),
    )
