from flask import Flask, render_template, redirect, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pytz

DATABASE_URI = 'mysql://root:@localhost/wechat'
IST = pytz.timezone('Asia/Kolkata')

app = Flask(__name__)
app.secret_key = 'SuperSecretKey'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
orm_session = Session()
orm_session._model_changes = {}

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

db = SQLAlchemy(app)


class AccountInfo(db.Model):
    __tablename__ = 'account_info'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(40), nullable=False)


class UserLogs(db.Model):
    __tablename__ = 'user_logs'
    id = db.Column(db.Integer, primary_key=True)
    last_activity = db.Column(db.DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now())
    shards = db.Column(db.Integer, nullable=False, server_default=func.now())


@app.route('/user/<id>/shards', methods=['GET'])
def user_shards(id):
    user = orm_session.query(UserLogs).filter_by(id=id).first()
    if user:
        if request.method == 'GET':
            aware_last_activity = IST.localize(user.last_activity)
            inactive_time = datetime.now(tz=IST) - aware_last_activity
            if inactive_time.total_seconds() >= 60:
                if user.shards < 48:
                    user.last_activity = datetime.now(tz=IST)
                    orm_session.commit()
                    return jsonify(shards=user.shards)
                user.shards -= 48
                user.last_activity = datetime.now(tz=IST)
                orm_session.commit()
            return jsonify(shards=user.shards)
    else:
        return jsonify(error='User not found'), 404


@app.route('/', methods=['GET', 'POST'])
def login_page():
    if 'user' in session:
        return redirect('/home')

    if request.method == 'POST':
        useremail = request.form.get('uEmail')
        userpass = request.form.get('uPassword')
        for i in orm_session.query(AccountInfo).all():
            if i.email == useremail:
                if i.password == userpass:
                    session['user'] = i.id
                    user = orm_session.query(UserLogs).filter_by(
                        id=session['user']).first()
                    updated_last_activity = datetime.now(tz=IST)
                    aware_last_activity = IST.localize(user.last_activity)
                    updated_shards = (updated_last_activity -
                                      aware_last_activity).total_seconds()//60
                    user.shards += updated_shards
                    if user.shards > 1440:
                        user.shards = 1440
                    user.last_activity = updated_last_activity
                    orm_session.commit()
                    if user.shards >= 48:
                        return redirect('/home')
                    else:
                        flash('Not Enough Shards', 'error')
                        return render_template('index.html')
                else:
                    flash('Invalid Password', 'error')
                    return render_template('index.html', shake=True)
        else:
            New = AccountInfo(email=useremail, password=userpass)
            orm_session.add(New)
            orm_session.commit()
            New_user = orm_session.query(
                AccountInfo).filter_by(email=useremail).first()
            logs = UserLogs(id=New_user.id)
            orm_session.add(logs)
            orm_session.commit()
            session['user'] = New_user.id
            return redirect('/home')

    return render_template('index.html')


@app.route('/home')
def home_page():
    if 'user' in session:
        return render_template('home.html', id=session['user'])
    return redirect('/')


@app.route('/logout/<id>')
def logout(id):
    user = orm_session.query(UserLogs).filter_by(id=id).first()
    updated_last_activity = datetime.now(tz=IST)
    user.last_activity = updated_last_activity
    orm_session.commit()
    session.pop('user')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
