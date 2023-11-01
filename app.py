import werkzeug.utils
from random_percentage import make_random_percentage
from sql_codes import insert_item_into_users, email_exist, token_check, remove_token, update_pass, load_post, add_product_to_basket, orders, remove_product, product_maker, adding_product
from hashing import calculate_md5
from token_jenerator import maker
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session


app = Flask(__name__)

not_login = True
token_s = False
email_login = ""
email = ""


@app.route('/', methods=['POST', 'GET'])
def home():
    global not_login, email_login
    not_login = True
    email_login = ""
    return render_template('index.html', not_login=not_login)


@app.route('/user', methods=['POST', 'GET'])
def user():
    if len(email_login) > 0:
        return render_template('index.html', not_login=not_login)
    else:
        return redirect('/login')


@app.route('/product', methods=['POST', 'GET'])
def product():
    product_list = product_maker()
    return render_template('product.html', product_list=product_list)


@app.route('/add_product', methods=['POST', 'GET'])
def add_product():
    stu = ""
    if len(email_login) > 0:
        name, desc, price, save_path = "", "", "", ""
        if request.method == "POST":
            name = request.form['name_']
            desc = request.form['desc_']
            price = request.form['price_']
        if 'img' in request.files:
            file = request.files['img']
            filename = werkzeug.utils.secure_filename(file.filename)
            if len(filename) >= 1:
                save_path = 'static/images/digiplus/' + filename
                file.save(save_path)
        if len(name) > 0 and len(desc) > 0 and len(price) > 0 and len(save_path) > 0:
            all_item = [name, desc, save_path, price, make_random_percentage()]
            adding_product(all_item)
            stu = "با موفقیت ثبت شد"
        return render_template('product_info.html', stu=stu)
    else:
        return redirect('/login')


@app.route('/product/post', methods=['POST', 'GET'])
def post():
    stu = ""
    if len(email_login) > 0:
        post_id = request.args.get('post_id')
        post = load_post(post_id)[0]
        if request.method == 'POST':
            product_id = request.args.get('post_id')
            add_product_to_basket(email_login, product_id)
            stu = "با موفقیت به سبد کالا ارسال شد"
        return render_template('post.html', post=post, stu=stu)
    else:
        return redirect('/login')


@app.route('/user/basket', methods=['POST', 'GET'])
def basket():
    global sum_product
    if len(email_login) > 0:
        if request.method == 'POST':
            keys = request.form
            product_id = []
            for i in keys.keys():
                product_id.append(i)
            remove_product(email_login, product_id[0])
        orders_from_customers = []
        for i in orders(email_login):
            orders_from_customers.append(load_post(i)[0])
        if len(orders_from_customers) == 0:
            not_full = True
        else:
            not_full = False
        sum_product = 0
        for i in orders_from_customers:
            sum_product += i[4]
        slicing = str(sum_product)[::-1]
        sliced = []
        finished_slicing = []
        index = 0
        for i in slicing:
            sliced.append(i)
        for i in sliced:
            index += 1
            finished_slicing.append(i)
            if index == 3:
                finished_slicing.append(",")
                index = 0
        finished_slicing.reverse()
        sum_product = "".join(finished_slicing)
        return render_template('basket.html', email_login=email_login, not_full=not_full, orders_from_customers=orders_from_customers, sum_product=sum_product)
    else:
        return redirect('/login')


@app.route('/pay', methods=['POST', 'GET'])
def pay():
    if len(email_login) > 0 and len(sum_product) > 0:
        return render_template('pay.html', sum_product=sum_product)
    elif len(email_login) == 0:
        return redirect('/login')


@app.route('/login', methods=['POST','GET'])
def login():
    global not_login, email_login
    stu = ""
    not_login = False
    if request.method == 'POST':
        email = request.form['email_']
        password = request.form['password_']
        try:
            data = email_exist(email)[0]
        except:
            stu = "همچین کاربری پیدا نشده یا رمز نادرست است"
        else:
            if calculate_md5(password) not in data:
                stu = "همچین کاربری پیدا نشده یا رمز نادرست است"
            elif calculate_md5(password) in data and email in data:
                email_login = email
                return redirect('/user')
    return render_template('register.html', stu=stu)


@app.route('/singup', methods=['POST','GET'])
def singup():
    global email
    stu = ""
    token_file = ""
    stu_email = False
    if request.method == 'POST':
        email = request.form['email_']
        password1 = request.form['password1_']
        password2 = request.form['password2_']
        try:
            data = email_exist(email)[0]
        except:
            if password1 == password2 and len(password1) >= 8 and len(password2) >= 8:
                password1 = calculate_md5(password1)
                insert_item_into_users(email, password1)
                maker(email)
                stu = "ثبت نام با موفقیت انجام شد"
                token_file = f"token({email}).txt"
                stu_email = True
            else:
                stu = "خطایی رخ داده است لطفا بررسی کنید رمز عبورتان بیش از 8 کارکتر باشد و رمز عبورتان به درستی تکرار شده است"
        else:   
            stu = "این ایمیل در سیستم وجود دارد لطفا از ایمیل دیگیری استفاده نمایید"
    return render_template('register_sing_up.html', stu=stu, token_file=token_file, stu_email=stu_email)


@app.route('/checking_email', methods=['POST','GET'])
def checking_email():
    global email
    stu = ""
    if request.method == 'POST':
        email = request.form['email_']
        try:
            data = email_exist(email)[0]
        except:
            stu = "همچین ایمیلی ثبت نشده است"
        else:
            email = email
            return redirect('/checking_email/code_checker')
    return render_template('checking_email.html', stu=stu)


@app.route('/checking_email/code_checker', methods=['POST','GET'])
def code_checker():
    global token_s, email
    stu = ""
    if len(email) == 0:
        return redirect('/checking_email')
    else:
        if request.method == 'POST':
            token = request.form['token_']
            if len(token) != 20:
                stu = "توکن باید 20 رقم باشد"
            elif token_check(email, token)[0][0] == "nop":
                stu = "توکن صحیح نیست"
            elif token_check(email, token)[0][0] == "ok":
                remove_token(token)
                token_s = True
                return redirect('/checking_email/code_checker/changepass')
    return render_template('token_checker.html', stu=stu)


@app.route('/checking_email/code_checker/changepass', methods=['POST','GET'])
def changepass():
    global token_s, email
    stu = ""
    if token_s:
        if request.method == 'POST':
            password1_ = request.form['password1_']
            password2_ = request.form['password2_']
            if password1_ == password2_ and len(password1_) >= 8 and len(password2_) >= 8:
                hash_pass = calculate_md5(password1_)
                update_pass(email, hash_pass)
                stu = "پسورد با موفقیت عوض شد"
                token_s = False
                email = ""
            else:
                stu = "خطایی رخ داده است لطفا بررسی کنید رمز عبورتان بیش از 8 کارکتر باشد و رمز عبورتان به درستی تکرار شده است"
        return render_template('change_pass.html', stu=stu)
    else:
        return redirect('/checking_email')


@app.route('/singup/download/<filename>', methods = ['GET'])
def download_token(filename):
    return send_from_directory('token', filename, as_attachment = True)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
