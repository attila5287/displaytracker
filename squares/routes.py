import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from squares import app, db, bcrypt
from squares.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, ItemForm, ItemDemo
from squares.models import User, Post, Item
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/inventory/home")
def inv_home():
    pass
    inventory = Item.query.all()

    try:
        _ = [item for item in inventory]
    except:
        inventory = []
    return render_template('inv_home.html', inventory=inventory, title='My Cars')


@app.route("/inventory/new", methods=['GET', 'POST'])
@login_required
def create_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(
            make=request.form["make"],
            model=request.form["model"],
            year=request.form["year"],
            body_type=request.form["body_type"],
            dest_id=request.form["dest_id"],
            ship_status=request.form["ship_status"],
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


# ============== CONTEXT_PROCESSORs

@app.context_processor
def inject_ItemDemoList():
    pass
    ItemDemoList = [
        ItemDemo(make=_make, model=_model, year=_year,
                 body_type=_bodyType, dest_id=_destId, ship_status=_shipStatus)
        for (_make, _model, _year, _bodyType, _destId, _shipStatus) in
        zip(
            [
                'Chrysler',
                'Mini',
                'Ford',
                'Toyota',
                'Hummer',
            ],
            [
                '300',
                'Cooper',
                'Mustang',
                'TRD',
                'H3',
            ],
            ['2011', '2012', '2013', '2014', '2015', ],
            ['0', '1', '2', '3', '4', ],
            ['0', '1', '2', '3', '4', ],
            ['0', '1', '2', '3', '4', ])]

    return dict(ItemDemoList=ItemDemoList)


@app.context_processor
def inject_destStyleDict():
    pass

    def destStyler(item_dest_index):
        pass
        destStyleDict = {
            '0': 'danger',
            '1': 'warning',
            '2': 'success',
            '3': 'info',
            '4': 'primary',
            '99': 'secondary',
        }
        return destStyleDict.get(item_dest_index, 'secondary')

    return dict(destStyler=destStyler)


@app.context_processor
def inject_bodyTypeImgDict():
    pass

    def imageFinder(item_bodyType_index):
        pass
        bodyTypeImgDict = {
            '0': '00.png',
            '1': '01.png',
            '2': '02.png',
            '3': '03.png',
            '4': '04.png',
        }
        return bodyTypeImgDict.get(item_bodyType_index, '00.png')

    return dict(imageFinder=imageFinder)


@app.context_processor
def inject_bodyTypeTextDict():
    pass

    def typeFinder(item_bodyType_id):
        pass
        bodyTypeTextDict = {
            '0': 'Sedan',
            '1': 'Compact',
            '2': 'Coupe',
            '3': 'Pickup',
            '4': 'SUV',
        }
        return bodyTypeTextDict.get(item_bodyType_id, 'UnknownBodyType')

    return dict(typeFinder=typeFinder)


@app.context_processor
def inject_shipStatMsgDict():
    pass

    def statusFinder(item_ship_status):
        pass
        shipStatMsgDict = {
            '0': 'not yet shipped',
            '1': 'receive next week',
            '2': 'receive following week',
            '3': 'receive within a month',
            '4': 'receive next month',
        }
        return shipStatMsgDict.get(item_ship_status, 'UnknownShipmentStatus')

    return dict(statusFinder=statusFinder)


@app.context_processor
def inject_destCityDict():
    pass

    def cityFinder(item_dest_id):
        pass
        destCityNameDict = {
            '0': 'Alabama',
            '1': 'Baltimore',
            '2': 'California',
            '3': 'Delaware',
            '4': 'Exeter',
        }
        return destCityNameDict.get(item_dest_id, 'UnknownDestinationCity')
    return dict(cityFinder=cityFinder)
