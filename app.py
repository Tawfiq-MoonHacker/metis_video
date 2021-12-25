from flask import Flask,flash, render_template, redirect, url_for,request,session
from flask_restful import Api,Resource
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
import get_contracts as gc
import ipfsApi
import base64

#datetime.strptime(result, '%Y-%m-%d %H:%M:%S.%f')

from dateutil.relativedelta import relativedelta
import sqlite3
import timeago
import email_validator
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import smtplib

import create_contract as cc
import secrets

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from file import forgot_password1,verification_email,return_username
import pymysql
from math import floor

from credentials import email_user, email_password,address_owner

import time
import os 
import threading

import json
from web3 import Web3

from sqlalchemy import create_engine


app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
bootstrap = Bootstrap(app)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['UPLOAD_FOLDER'] = 'static/videos/'
# ALLOWED_EXTENSIONS = set(['mp4'])

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

metis_network = "https://andromeda.metis.io/?owner=1088"
client = ipfsApi.Client('127.0.0.1', 5001) 


def moveDecimalPoint(num, decimal_places):
    for _ in range(abs(decimal_places)):

        if decimal_places>0:
            num *= 10; #shifts decimal place right
        else:
            num /= 10.; #shifts decimal place left

    return float(num)


s = URLSafeTimedSerializer('Thisisasecret!')

# {"secret_api": "", "video" : "" ,"name": "here it goes","address":"address"}

class add_video(Resource):
    def post(self,public_api):
        
        try:
            address = request.form['address']
            if gc.check_api(address,request.form['secret_api'],public_api):
                
                file = request.form["video"]
                
                size = len(file)
                
                if gc.get_GB(address) * (10**9) < size:
                    return "size is bigger than the available/ not subscribed "
                
                else:
                    # client = ipfsApi.Client('127.0.0.1', 5001) 
                    path = os.path.join(app.config['UPLOAD_FOLDER'],"video.mp4")
                    file.save(path)
        
                    added = client.add("static/videos/video.mp4")[0]
                    
                    
                    set_GB(((get_GB(address) * (10**9)) - int(added['Size']))/(10**9))
                    
                    hashes = added['Hash']
                    
                    gc.add_video(hashes,address,str(datetime.now()),request.form['name'],secrets.token_urlsafe(18))
                    
                    
                    
                    
        except:
            return {"failed":500}
        
        return {"success":200}
    
api.add_resource(add_video,"/add_video/<string:public_api>")

# {"secret_api": "","token_video": "here it goes","address","address}

class delete_video(Resource):
    def post(self,public_api):
       
        try:
            address = request.form['address']
            token = request.form['token_video']
            
            if gc.check_api(address,request.form['secret_api'],public_api):
                
                video = Video.query.filter_by(token_video = request.form['token_video']).first()
                
                result = client.cat(gc.get_sha(user.address,video.contract_address))
    
                gc.set_GB(((gc.get_GB(address) * (10**9)) + len(result)) / (10**9))
                
                num_videos = gc.num_videos(address)
                
                for i in range(num_videos):
                    if gc.getvideo(address,i)[3] == token:
                        gc.delete_video(address,i)
                        break
                    
        except:
            return {"failed":500}
        
        return {"success":200}
    
api.add_resource(delete_video,"/delete_video/<string:public_api>")


# {"secret_api": "","address","address"}

class get_videos(Resource):
    def post(self,public_api):
        
        
        try:
            if gc.check_api(address,request.form['secret_api'],public_api):
                videos = {'videos':[]}
                
                num_videos = gc.num_videos(address)
                
                video = Video.query.filter_by(address = user.address).all()
                
                for i in range(num_videos):
                    num = i
                    list1 = {}
                    video = gc.get_video(address,i)
                    
                    list1['num'] = num
                    list1['name'] = video[1].name
                    list1['url'] = '/video/' + video[3]
                    list1['token'] = video[3]
                    
                    list1['date'] = str(datetime.strptime(video[2], '%Y-%m-%d %H:%M:%S.%f').strftime("%b %d, %Y %H:%M:%S"))[0:-7]
                    
                    videos['videos'].append(list1)
                
                return videos
            
        except:
            return {"failed":500}
        
        return {"success":200}

#reutrns {'videos':[{'num':1,'name':"name1",'url':"/video/343293842u","token":"asf3kfj","date":"2022/1/1"}]}    
api.add_resource(get_videos,"/get_videos/<string:public_api>")




def send(subject,content,file,email_send):
    
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject
    

    msg.attach(MIMEText(content,'html'))
    
    
    if file != None:
        filename= file
        attachment  =open(filename,'rb')
    
        part = MIMEBase('application','octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',"attachment; filename= "+filename)
    
        msg.attach(part)
        
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)
    
    
    server.sendmail(email_user,email_send,text)
    server.quit()
    

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    address = db.Column(db.String(4000),unique = True)
    private_address = db.Column(db.String(4000),unique = True)
    
    balance = db.Column(db.Float,default = 0.000000)
    token = db.Column(db.String(2000),default = None)
    
    end_date = db.Column(db.DateTime,default = None)
    GB = db.Column(db.Float,default = 0)
    
    verification = db.Column(db.Boolean,default = False)
    public_api = db.Column(db.String(2000),default = '0')
    secret_api = db.Column(db.String(2000),default= '0')
    
    
class Video(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    token_video = db.Column(db.String(4000),unique = True)
    name = db.Column(db.String(4000),unique=False)
    contract_address = db.Column(db.String(4000),unique = False)
    address = db.Column(db.String(4000),unique=False)
    date = db.Column(db.DateTime,default= datetime.now())
    

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id = user_id).first()
    
    
    if user:         
        try:

            w3 = Web3(Web3.HTTPProvider(metis_network))

            #it checks if there is a payment
            balance = w3.eth.get_balance(user.address)
            user.balance = moveDecimalPoint(balance,-18)
            
            try:
                if user.end_date < datetime.now():
                    user.GB = 0.0
                    
                    delete_q = Video.__table__.delete().where(Video.address == user.address)
                    
                    db.session.execute(delete_q)
                    db.session.commit()
            except:
                pass
            
                
            db.session.commit()
            
            
            
            return User.query.get(int(user_id))
        except Exception as e:
            pass
        

    
    


def render_frame(arr):
    img_base64 = base64.b64encode(arr).decode('ascii')
    mime = "video/mp4"
    uri = "data:%s;base64,%s"%(mime, img_base64)
    
    return render_template("main.html",video=uri)



@app.route("/video/<string:token>",methods=['GET'])
def video(token):
    addresses = gc.get_addresses()
    hash = ''
    
    for i in addresses:
        num_videos = gc.num_video(i)
        for j in range(num_videos):
            if gc.getvideo(i,j)[3] == token:
                hash = gc.getvideo(i,j)[0]
    
    result = client.cat(hash)
    return render_frame(result)

    else:
        return "nothing"


@app.route('/')
def index():
    
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login(username = None):
    form = LoginForm()
    
    if username != None:
        user = User.query.filter_by(username = username).first()
        login_user(user)

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data) and user.verification == True:
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
    if request.method == 'POST':
        
        user = User.query.filter_by(email = form.username.data).first()
        if user:
            if check_password_hash(user.password,form.password.data) and user.verification == True:
                login_user(user,remember=form.remember.data)
                return redirect(url_for('dashboard'))
            
            if user.verification == False:
                token = s.dumps(user.email, salt='email-confirm')
                
                link = url_for('confirm_email', token=token, _external=True)
                
                user.token = token
                
                db.session.commit()
        
                content = verification_email(link)
                subject = "here is your verification "
            
                send(subject, content,None,form.email.data)
                
                return render_template("verify-email.html")
            
            
            return render_template('login.html',form = form,wrong = True)
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form,wrong = False)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        
        w3 = Web3(Web3.HTTPProvider(metis_network))
        
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        email = request.form['email']
        token = s.dumps(email, salt='email-confirm')

        acct = w3.eth.account.create()
        public_api = secrets.token_urlsafe(18)
        secret_api = secrets.token_urlsafe(18)

        print(acct.address)
        print(acct.key.hex())
        
        gc.add_user(form.username.data,form.email.data,form.password.data,acct.address,token,acct.key.hex(),secret_api,public_api)
        
        link = url_for('confirm_email', token=token, _external=True)


        content = verification_email(link)
        subject = "here is your verification "
    
        send(subject, content,None,form.email.data)
        
        return render_template("verify-email.html")
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html',form = form)


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=300)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    
    user = User.query.filter_by(token = token).first()
    if user:
        user.verification = True
        
        db.session.commit()
        
        return login(username = user.username)
    
    else:
        return "retry again"

@app.route('/forgot_password',methods=['POST','GET'])
def forgot_password():
    if request.method == 'POST':
        
        email = request.form['email']
        token = s.dumps(email, salt='reset-password')
        
        try:
            user = User.query.filter_by(email = email).first()
            user.token = token
            db.session.commit()
        except:
            return render_template("forgot_password.html")
        
        
        
        link = url_for('reset_password', token=token, _external=True)
        content =  forgot_password1(link)
        subject = "reset your password"
    
        send(subject, content,None,email)
        
        return render_template("link_sent.html")
        
    return render_template("forgot_password.html")

@app.route('/forgot_username',methods=['POST','GET'])
def forgot_username():
    if request.method == 'POST':
        
        email = request.form['email']
        token = s.dumps(email, salt='reset-password')
        name = ""
        
        try:
            user = User.query.filter_by(email = email).first()
            name = user.username
            db.session.commit()
        except:
            return render_template("forgot_username.html")
        
        
        content =  return_username(name)
        subject = "Username Reveal"
    
        send(subject, content,None,email)
        
        return render_template("link_sent.html")
        
    return render_template("forgot_username.html")


@app.route('/reset_password/<token>',methods=['POST','GET'])
def reset_password(token,link = None):
    
    form = LoginForm()

    if request.method == 'POST':
        user = User.query.filter_by(token = token).first()
        if user:
            user.password = generate_password_hash(form.password.data, method='sha256')
            db.session.commit()
            return login(user.username)
        
    if request.method == 'GET':
        user = User.query.filter_by(token = token).first()
        try:
            email = s.loads(token, salt='reset-password', max_age=300)
            link = url_for('reset_password', token=token, _external=True)
            return render_template("reset_password.html",link = link,form = form)

        except SignatureExpired:
            return '<h1>The token is expired!</h1>'
    


@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.filter_by(username = current_user.username).first()
    
    
    time = user.end_date
    if time != None:
        time = time.strftime("%b %d, %Y %H:%M:%S")
        # time = str(time)[0:-7]
        
        
    return render_template('dashboard.html', name=current_user.username,time = time)


@app.route('/dashboard/payments')
@login_required
def payment():
    
    name = current_user.username
        
    user = User.query.filter_by(username = current_user.username).first()
    address = user.address
    balance = user.balance
    
    time = user.end_date
    if time != None:
        time = time.strftime("%b %d, %Y %H:%M:%S")
        # time = str(time)[0:-7]
        
    return render_template('payments.html',name = name,balance = balance,address = address,time=time,text=None)
    

@app.route('/adding_video',methods=['POST','GET'])
@login_required
def adding_video():
    
    user = User.query.filter_by(username = current_user.username).first()
    address = user.address

    time = user.end_date
    if time != None:
        time = time.strftime("%b %d, %Y %H:%M:%S")
        # time = str(time)[0:-7]
        
    if request.method == 'POST':
            
        file = request.files['file']
        
        path = os.path.join(app.config['UPLOAD_FOLDER'],"video.mp4")
        file.save(path)
                
        if 'file' not in request.files:
            print('there is no file in form!')
            return redirect(request.url)
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        blob = file.read()
        size = len(blob) # in bytes 
        
        if user.GB * (10**9) < size:
            return render_template("adding_video.html",name = user.username,time=time,size_left = user.GB)
        

        else:
            added = client.add('static/videos/video.mp4')[0]
            print(added)
            
            user.GB = ((user.GB * (10**9)) - float(added['Size']))/(10**9)

            hashes = added['Hash']
            
            contract_address = cc.create_contract(user.address,hashes)
            
            db.session.commit()
            
            video = Video(token_video = secrets.token_urlsafe(18),name = file.filename,contract_address = contract_address,address = address,date = datetime.now())

            
            db.session.add(video)
            db.session.commit()
                
        
    
    return render_template("adding_video.html",name = user.username,time=time,size_left = user.GB)


@app.route('/my_videos',methods=['POST','GET'])
@login_required
def my_videos():
    
    user = User.query.filter_by(username = current_user.username).first()
    address = user.address
    
    video = Video.query.filter_by(address = address).all()
    
    time = user.end_date
    if time != None:
        time = time.strftime("%b %d, %Y %H:%M:%S")
        # time = str(time)[0:-7]
        
    if video:
        videos = []
        
        for k,i in enumerate(video):
            num = k-1
            list1 = []
            list1.append(num+2)
            list1.append(video[num].name)
            list1.append('/video/' + video[num].token_video)
            list1.append(str(video[num].date.strftime("%b %d, %Y %H:%M")))
            
            videos.append(list1)
            
    
        return render_template("my_videos.html",name = user.username,nothing = False,videos = videos,time=time)
    
    else:
        return render_template("my_videos.html",name = user.username,nothing = True,time=time)

@app.route('/video/<token>/delete',methods=['GET'])
@login_required
def video_delete(token):
    
    user = User.query.filter_by(username = current_user.username).first()
    address = user.address
    
    video = Video.query.filter_by(token_video = token).first()
    
    # client = ipfsApi.Client('127.0.0.1', 5001) 
    
    # print(gc.get_sha(address,video.contract_address))
    
    # result = client.cat(gc.get_sha(address,video.contract_address))
    
    # user.GB = ((user.GB * (10**9)) + len(result)) / (10**9)
    # db.session.commit()

    delete_q = Video.__table__.delete().where(Video.token_video == token)
    db.session.execute(delete_q)
    db.session.commit()
        
    return redirect(url_for('my_videos'))


@app.route('/transfer',methods=['POST','GET'])
@login_required
def transfer():
    
    user = User.query.filter_by(username = current_user.username).first()
    # payment = Payments.query.filter_by(username = current_user.username).first()
    private_address = user.private_address
    address_send = user.address
    
    time = user.end_date
    if time != None:
        time = time.strftime("%b %d, %Y %H:%M:%S")
        # time = str(time)[0:-7]
        
    if request.method == 'POST':
        quantity = float(request.form['quantity'])
        address_recv = request.form['address']
        
        gc.transfer_coins(address_send,address_recv,private_address,float(quantity))
    
        return redirect(url_for('dashboard'))
    else:
        return render_template('transfer.html',name = current_user.username,time=time)


@app.route('/api',methods=['POST','GET'])
@login_required
def api():
    user = User.query.filter_by(username = current_user.username).first()
    
    time = user.end_date
    if time != None:
        time = time.strftime("%b %d, %Y %H:%M:%S")
        # time = str(time)[0:-7]
    
    if request.method == "GET":
        try:
                
            if user:
                public_api = user.public_api
                secret_api = user.secret_api
                
                    
                return render_template('api.html',name = current_user.username, public_api = public_api,secret_api = secret_api,time=time)
            
        except:
            return redirect(url_for('dashboard'))
        
    else:
        user.public_api = secrets.token_urlsafe(18)
        user.secret_api = secrets.token_urlsafe(18)
        
        public_api = user.public_api
        secret_api = user.secret_api
                    
        db.session.commit()
        
        return render_template('api.html',name = current_user.username, public_api = public_api,secret_api = secret_api,time=time)


@app.route('/dashboard/1month',methods=['POST','GET'])
@login_required
def dashboard_1month():
    user = User.query.filter_by(username = current_user.username).first()

    site = '/dashboard/1month'
    
    time = user.end_date
    if time != None:
        time = time.strftime("%b %d, %Y %H:%M:%S")
        # time = str(time)[0:-7]
    
    if request.method == 'GET':
        
    
        
        return render_template('subscription.html',name = current_user.username,time=time,value=0.07,site=site)
    
    elif request.method == 'POST':
        try:
            quantity = float(request.form['GB'])
            
            if user.balance > quantity * 0.07:
                
                user.end_date = datetime.now() + relativedelta(months=1)
                user.GB = float(quantity) + user.GB
                
            else:
                balance = user.balance 
                address = user.address

                return render_template("payments.html",name = name,balance = balance,address = address,time=time,text= "you need to deposit ")
           
            #sending coins from buyer to the owner of the website

            gc.transfer_coins(user.address,address_owner,user.private_address,float(request.form['GB']) * 0.07)
            db.session.commit()

        except:
            return render_template('subscription.html',name = current_user.username,time=time,value=0.07,site=site)
        
        return redirect(url_for('my_videos'))



if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.run(debug=True)
    

