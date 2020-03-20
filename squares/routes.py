import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from squares import app, db, bcrypt
from squares.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, ItemForm 
from squares.models import User, Post, ItemDemo
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
    # inventory = Item.query.all()
    inventory = []

    try:
        _ = [item for item in inventory]
    except:
        inventory = []
    return render_template('inv_home.html', inventory=inventory, title='Yuupon')


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


# ============== UPLOAD ALL YUUPONG HATS ~100

@app.context_processor
def inject_ItemDemoList():
    pass
    base_url = 'https://shop.flexfit.com/product/image/medium/'

    ItemDemoList = [
        ItemDemo(
            id='9999',
            manufacturer='YUUPONG',
            catalog_no=catalog_no,
            catalog_desc=catalog_desc,
            image_url=base_url+image_url,
        )
        for (catalog_no, catalog_desc, image_url) in
        zip(
            [
                " 110C",
                " 110F",
                " 110FT",
                " 110M",
                " 110MT",
                " 110P",
                " 110R",
                " 110RT",
                " 1500KC",
                " 1501KC",
                " 1501P",
                " 1525CM",
                " 1535TH",
                " 1545K",
                " 180",
                " 2006",
                " 280",
                " 360",
                " 360T",
                " 5001",
                " 5089M",
                " 5789M",
                " 6002",
                " 6005FF",
                " 6005FW",
                " 6006",
                " 6006MC",
                " 6006T",
                " 6006W",
                " 6007",
                " 6007T",
                " 6089CM",
                " 6089M",
                " 6089MC",
                " 6089MT",
                " 6089TC",
                " 6161",
                " 6195P",
                " 6196",
                " 6197",
                " 6210",
                " 6245CM",
                " 6245MC",
                " 6245PT",
                " 6262SV",
                " 6277",
                " 6277MC",
                " 6277T",
                " 6277XX",
                " 6277Y",
                " 6297F",
                " 6311",
                " 6320",
                " 6320W",
                " 6350",
                " 6355",
                " 6360",
                " 6360T",
                " 6363V",
                " 6377",
                " 6477",
                " 6502",
                " 6506",
                " 6506T",
                " 6511",
                " 6511MC",
                " 6511T",
                " 6511W",
                " 6530",
                " 6533",
                " 6533T",
                " 6560",
                " 6572",
                " 6577CD",
                " 6580",
                " 6584",
                " 6587",
                " 6597",
                " 6606",
                " 6606CA",
                " 6606MC",
                " 6606R",
                " 6606RT",
                " 6606T",
                " 6606W",
                " 6689",
                " 6745",
                " 6789M",
                " 6988",
                " 6997",
                " 6997Y",
                " 6999",
                " 7005 "
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
            [
                "110c_rd_1.jpg",
                "110f_wh_1.jpg",
                "110ft_bkrd_1.jpg",
                "110m_bk_1.jpg",
                "110mt_nvwh_1.jpg",
                "110p_rd_1.jpg",
                "110r_bk_1.png",
                "110rt_bkwh_1.png",
                "1500kc_pr_1.jpg",
                "1501kc_cb_1.jpg",
                "1501p_dg_1.jpg",
                "1525cm_bk_1.jpg",
                "1535th_sr_1.jpg",
                "1545k_dg_1.jpg",
                "180_sv_1.png",
                "2006_bk_1.jpg",
                "280_mlbk_1.jpg",
                "360_no_1.jpg",
                "360t_rdwh_1.jpg",
                "5001_nv_1.jpg",
                "5089m_wh_1.jpg",
                "5789m_nv-one_1.jpg",
                "6002_nv_1.jpg",
                "6005ff_nv_1.jpg",
                "6005fw_rywhry_1.jpg",
                "6006_bk_1.jpg",
                "6006MC_6006MC_MULTICAM_LEFT_SLANT_STICKER1.png",
                "6006T_6006T_CHBK_1.jpg",
                "6006W_6006W_rdwhrd_1.png",
                "6007_gr_1.jpg",
                "6007t_bkrd_1.jpg",
                "6089cm_gn_1.jpg",
                "6089m_sp_1.jpg",
                "6089mc_al_1.jpg",
                "6089mt_bkrd_1.jpg",
                "6089tc_bkca_1.jpg",
                "6161_nvwh_1.jpg",
                "6195p_bk_1.jpg",
                "6196_bkwh_1.jpg",
                "6197_bkgn_1.jpg",
                "6210_dg_1.jpg",
                "6245cm_kh_1.jpg",
                "6245mc_al_1.png",
                "6245pt_ll_1.jpg",
                "6262sv_mrnv_1.jpg",
                "6277_st_1.jpg",
                "6277mc_ar_1.jpg",
                "6277t_bkrd_1.jpg",
                "6277xx_br_1.jpg",
                "6277y_ry_1.jpg",
                "6297f_nv_1.jpg",
                "6311_hebk_1.jpg",
                "6320_wh_1.jpg",
                "6320w_bkwhbk_1.jpg",
                "6350_mlsv_1.jpg",
                "6355_dh_1.jpg",
                "6360_rd_1.jpg",
                "6360t_chwh_1.jpg",
                "6363v_nv_1.jpg",
                "6377_nv_1.jpg",
                "6477_mr_1.jpg",
                "6502_bk_1.jpg",
                "6506_nv_1.jpg",
                "6506t_rdwh_1.jpg",
                "6511_dn_1.jpg",
                "6511mc_bk_1.jpg",
                "6511t_chwh_1.jpg",
                "6511w_nvwhnv_1.jpg",
                "6530_wh_1.jpg",
                "6533_dg_1.jpg",
                "6533t_nvwh_1.jpg",
                "6560_wh_1.jpg",
                "6572_kh_1.jpg",
                "6577cd_ry_1.jpg",
                "6580_bk_1.jpg",
                "6584_nv_1.jpg",
                "6587_wh_1r.jpg",
                "6597_wh_1.jpg",
                "6606_rd_1.jpg",
                "6606ca_gc_1.jpg",
                "6606mc_mc_1.jpg",
                "6606r_bk_1.png",
                "6606rt_bkwh_1.png",
                "6606t_rukh_1.jpg",
                "6606w_bkwhb_1.jpg",
                "6689_dg_1.jpg",
                "6745_nv_1.jpg",
                "6789m_he_1.jpg",
                "6988_kn_1.jpg",
                "6997_nv_1.jpg",
                "6997y_ry_1.jpg",
                "6999_bu_1.jpg",
                "7005_dg_1.jpg",
            ],
        )
    ]
    print(*ItemDemoList)

    return dict(ItemDemoList=ItemDemoList)
  