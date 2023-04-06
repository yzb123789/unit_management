from email import message
from models import EmailCaptchaModel
from exist import mail,db
from flask import Blueprint,render_template,request,jsonify,redirect,url_for,session
from flask_mail import Message
import string,random
from .forms import LoginForm,RegisterForm
from models import Usermodel
from werkzeug.security import generate_password_hash,check_password_hash

bp=Blueprint("user",__name__,url_prefix="/user")
@bp.route("/login",methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template("login.html")
    else:
        form=LoginForm(request.form)
        if form.validate():
            email=form.email.data
            password=form.password.data
            user=Usermodel.query.filter_by(email=email).first()
            if not user:
                return render_template(url_for("user.login"))
            if check_password_hash(user.password,password):
                session['user_id']=user.id
                return redirect("/")
            else:
                return render_template(url_for("user.login"))
        else:
            print(form.errors)
            return redirect(url_for("user.login"))
@bp.route("/register",methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template("register.html")
    else:
        form=RegisterForm(request.form)
        if form.validate():
            email=form.email.data
            username=form.username.data
            password=form.password.data
            user = Usermodel(email=email,username=username,password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            print(form.errors)
            return redirect(url_for("user.register"))

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("user.login"))

@bp.route("/captcha/email")
def get_email_captcha():
    email=request.args.get("email")
    source=string.digits*4
    captcha=random.sample(source,4)
    captcha=captcha[0]+captcha[1]+captcha[2]+captcha[3]
    message=Message(subject="注册验证码",recipients=[email],body=f"您的验证码是：{captcha}")
    mail.send(message)
    email_captcha=EmailCaptchaModel(email=email,captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({"code":200,"message":"","data":None})

@bp.route("/mail/test")
def mail_test():
    message=Message(subject="ceshi",recipients=["1624936525@qq.com"],body="ceshi")
    mail.send(message)
    return "success"

