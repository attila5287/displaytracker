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
    User, Post, ItemDemo, Item
)
from flask_login import (
    login_user, current_user, logout_user, login_required
)


@app.route("/inventory/list")
def inv_lister():
    pass

    inventory = Item.query.all()

    try:
        _ = [item for item in inventory]
    except:
        inventory = []
    return render_template('inv_lister.html', inventory=inventory, title='InvDemoListRandData')

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

@app.route('/square00')
def square_00():
    return render_template('square_00.html', title='Square 00')

@app.route("/inventory/home")
def inv_home():
    pass

    inventory = Item.query.all()

    try:
        _ = [item for item in inventory]
    except:
        inventory = []
    return render_template('inv_home.html', inventory=inventory, title='InvDemoRandCol')

@app.route("/")
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
        item = Item(
            manufacturer=request.form["manufacturer"],
            catalog_no=request.form["catalog_no"],
            catalog_fullname=request.form["catalog_fullname"],
            imagewhtbg_url=request.form["imagewhtbg_url"],
            imageclean_url=request.form["imageclean_url"],
            color_primary=request.form["color_primary"],
            color_secondary=request.form["color_secondary"],
            product_url=request.form["product_url"],
            is_adjustable=request.form["is_adjustable"],
            is_flexfit=request.form["is_flexfit"],
            is_youth=request.form["is_youth"],
            is_fitted=request.form["is_fitted"],
            has_structcrwn=request.form["has_structcrwn"],
            has_curvedbill=request.form["has_curvedbill"],
            has_flatbill=request.form["has_flatbill"],
            inv_lowinstock=request.form["inv_lowinstock"],
            inv_outofstock=request.form["inv_outofstock"],
        )
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
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
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

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
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
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

# demo objects (no db) yupoong trns-png'ed items ~100
@app.context_processor
def inject_ItemDemoList():
    pass
    # base_url = 'https://shop.flexfit.com/product/image/medium/'
    base_url = 'https://raw.githubusercontent.com/attila5287/displaytracker_img/master/yupoong/image_clean/'
    
    # 110C
    end_url = '.png'

    ItemDemoList = [
        ItemDemo(
            id = '9999',
            manufacturer = 'YUUPONG',
            catalog_no=str(catalog_no).lstrip(),
            catalog_desc = catalog_desc,
            image_url = base_url + catalog_no + end_url,
        )
        for (catalog_no, catalog_desc) in
        zip(
            [
                "110C",
                "110F",
                "110FT",
                "110M",
                "110MT",
                "110P",
                "110R",
                "110RT",
                "1500KC",
                "1501KC",
                "1501P",
                "1525CM",
                "1535TH",
                "1545K",
                "180",
                "2006",
                "280",
                "360",
                "360T",
                "5001",
                "5089M",
                "5789M",
                "6002",
                "6005FF",
                "6005FW",
                "6006",
                "6006MC",
                "6006T",
                "6006W",
                "6007",
                "6007T",
                "6089CM",
                "6089M",
                "6089MC",
                "6089MT",
                "6089TC",
                "6161",
                "6195P",
                "6196",
                "6197",
                "6210",
                "6245CM",
                "6245MC",
                "6245PT",
                "6262SV",
                "6277",
                "6277MC",
                "6277T",
                "6277XX",
                "6277Y",
                "6297F",
                "6311",
                "6320",
                "6320W",
                "6350",
                "6355",
                "6360",
                "6360T",
                "6363V",
                "6377",
                "6477",
                "6502",
                "6506",
                "6506T",
                "6511",
                "6511MC",
                "6511T",
                "6511W",
                "6530",
                "6533",
                "6533T",
                "6560",
                "6572",
                "6577CD",
                "6580",
                "6584",
                "6587",
                "6597",
                "6606",
                "6606CA",
                "6606MC",
                "6606R",
                "6606RT",
                "6606T",
                "6606W",
                "6689",
                "6745",
                "6789M",
                "6988",
                "6997",
                "6997Y",
                "6999",
                "7005"
            ],
            [
                "Flexfit 110 Pro-Formance",
                "One Ten Snapback",
                "One Ten Snapback 2-Tone",
                "FLEXFIT 110 MESH CAP",
                "110 TRUCKER 2-TONE",
                "One Ten Cool & Dry Mini Pique",
                "RECYCLED 110 FITTED",
                "RECYCLED 110 FITTED 2-TONE",
                "Heavyweight Beanie Knit",
                "Heavyweight Cuffed Beanie Knit",
                "Cuffed Beanie Knit with Pom Pom",
                "Cool Max Beanie",
                "Thinsulate Cuffed Beanie",
                "Ribbed Cuffed Knit",
                "Flexfit Delta Seamless Cap",
                "Polar Fleece Beanie",
                "Flexfit Delta Unipanel Knit Cap",
                "360 Full Mesh Flexfit",
                "360 Full Mesh Flexfit 2-TONE",
                "V-Flexfit Cotton Twill",
                "Premium 5 Panel Snapback",
                "5PNL CURVED VISOR SNAPBACK",
                "Poplin Golf Snapback",
                "Foam Trucker",
                "White Front Foam Trucker",
                "5 PANEL Classic Trucker",
                "5 PANEL MULTICAM TRUCKER",
                "5 PANEL Classic Trucker 2-Tone",
                "5 panel Classic Trucker/ White Front",
                "5 Panel Cotton Twill Snapback",
                "5 Panel Cotton Twill Snapback 2-Tone",
                "GREEN CAMO SNAPBACK",
                "Premium 6 Panel Classic Snapback Wool Blend",
                "SNAPBACK MULTICAM",
                "Premium 6 Panel Classic 2-Tone Snapback",
                "Classic 2-Tone Snapback with Camo",
                "Brushed Cotton Twill with Transvisor",
                "Flexfit Pinstripe",
                "Flexfit Glen Check",
                "Flexfit Tartan Plaid",
                "Premium 210 Fitted",
                "Unstructured Low Profile Cotton Twill",
                "MULTICAM DAD HAT",
                "Peached Cotton Twill Dad Cap",
                "Brushed Cotton Sandwich Visor",
                "Flexfit Wooly Combed Twill",
                "FLEXFIT MULTICAM",
                "Flexfit Wooly Combed 2-Tone",
                "Flexfit Wooly Combed Extra Extra Large",
                "Flexfit Wooly Combed Youth",
                "Flexfit Pro-Baseball On Field Twill",
                "Flexfit Melange Trucker Mesh",
                "FOAM TRUCKER CURVED VISOR",
                "FOAM TRUCKER CURVED VISOR WHITE FRONT PANEL",
                "FINE MELANGE FLEXFIT",
                "Flexfit Melange Cap",
                "360 Full Mesh Ajustable",
                "360 Full Mesh Adjustable 2-Tobe",
                "Brushed Cotton Twill Mid Profile",
                "Flexfit Brushed Twill",
                "Flexfit Wool Blend",
                "Unstructured 5 Panel Snapback",
                "5 PANEL RETRO YUPOONG TRUCKER",
                "5 PANEL RETRO TRUCKER 2TONE",
                "Flexfit Trucker Mesh",
                "Flexfit Multicam Trucker Mesh",
                "Flexfit Trucker Mesh 2-Tone",
                "Flexfit Trucker White Front",
                "Flexfit Ultrafibre",
                "Flexfit Ultrafibre Airmesh",
                "Flexfit Ultrafibre Airmesh 2 Tone",
                "Flexfit Five Panel",
                "Flexfit Cool & Dry Calocks Tricot",
                "Flexfit Cool & Dry Pique Mesh",
                "Flexfit Pro-Formance",
                "FLEXFIT COOL & DRY 3D HEXAGON JERSEY CAP",
                "FLEXFIT HYDRO GRID CAP",
                "Flexfit Cool & Dry Sport",
                "6 PANEL Retro Trucker",
                "Retro Yupoong Trucker Camo",
                "6 PANEL MULTICAM TRUCKER",
                "Recycled 6 Pnl Trcuker",
                "Recycled 6 Pnl Trucker 2-Tone",
                "6 PANEL Retro Trucker 2-Tone",
                "6 PANEL Trucker/ White Front",
                "Melton Wool Snapback",
                "Flexfit Cotton Twill Dad Hat",
                "PREMIUM CURVED VISOR YUPOONG SNAPBACK",
                "Flexfit® TrueTimber® Kanati Camo",
                "Flexfit Garment Washed Cotton",
                "Flexfit Garment Washed Cotton Youth",
                "Flexfit Mossy Oak",
                "Classic Jockey Camper",
            ],
            
        )
    ]
    # print(*ItemDemoList)

    return dict(ItemDemoList=ItemDemoList)

@app.context_processor
def inject_headers():
    ''' GENERATES A LIST OF ITEM ATTIRIBUTES TO BE USED AS TABLE HEADERS '''
    pass
    _list = [
        "imagewhtbg_url", 
        "imageclean_url", 
        "id", 
        "manufacturer",
        "catalog_fullname", 
        "color_primary", 
        "color_secondary", 
        "inv_lowinstock", 
        "inv_outofstock", 
        "is_snapback", 
        "is_adjustable", 
        "is_flexfit", 
        "is_youth", 
        "is_fitted", 
        "has_structcrwn", 
        "has_curvedbill", 
        "has_flatbill",
    ]
    DisplayHeaders = [
        header for header in _list
    ]
    return dict(DisplayHeaders=DisplayHeaders)
