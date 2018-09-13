from flask import Flask, request, jsonify, session, render_template, redirect, url_for, send_from_directory
from model import User, UserSchema, RoleSchema, Session
from passlib.hash import argon2
from marshmallow import pprint
from utils import is_logged, is_admin, required_params_are_ok
from mail import mail_login, mail_passwd_update, mail_user_created

import json
import os


from wgsi import app

db_session = Session()

user_schema = UserSchema(only=('id', 'login', 'role', 'mail'))
users_schema = UserSchema(only=('id', 'login', 'role', 'mail'), many=True)
roles_schema = RoleSchema(many=True)

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/<string:page_name>/')
def caveat(page_name):
  return redirect(url_for('home'), code=302)


@app.route('/')
def home():
  if 'login' not in session:
    return render_template('login.html')
  else:
    if 'role' not in session:
      return "Somthg is wrong with your session"
    elif session['role'] == 'administrator':
      return render_template('admin.html', login=session['login'], users='USERS')
    elif session ['role'] == 'default':
      return render_template('self.html', login=session['login'])
    else:
      return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
  expected = ('login', 'password')
  try:
    dicted_data = required_params_are_ok(request, expected)
  except ValueError as err:
    return str(err)

  login = dicted_data['login']
  password = dicted_data['password']

  if 'login' in session:
    return redirect(url_for('home'), code=302)

  user = db_session.query(User).filter(User.login == login).first()
  if user and argon2.verify(password, user.password) == True:
    session['login'] = user.login
    session['id'] = user.id
    session['role'] = user.role.name
    #mail_login(user.mail)
    return 'Session initiated {}'.format(session)
  else:
    return 'Bad credentials'


@app.route("/users", methods=["POST"])
def add_user():
  expected = ('login', 'password', 'id_role', 'mail')
  try:
    dicted_data = required_params_are_ok(request, expected)
    is_logged()
    is_admin()
  except ValueError as err:
    return str(err)

  login = dicted_data['login']
  mail = dicted_data['mail']
  password = argon2.hash(dicted_data['password'])
  id_role = dicted_data['id_role']

  user = db_session.query(User).filter(User.login == login).first()

  if user:
    return "Login already taken"

  new_user = User(login, password, id_role, mail)

  db_session.add(new_user)
  db_session.commit()
  db_session.refresh(new_user)

  #mail_user_created(new_user.mail, new_user.login, dicted_data['password'])

  epure = user_schema.dumps(new_user)
  return jsonify(epure.data)


@app.route("/users", methods=["GET"])
def get_user():
  all_users = db_session.query(User).all()
  result = users_schema.dumps(all_users)
  return jsonify(result.data)


@app.route("/self", methods=["POST"])
def update_self():
  expected = ('password', 'new_password')
  try:
    dicted_data = required_params_are_ok(request, expected)
    is_logged()
  except ValueError as err:
    return str(err)

  password = dicted_data['password']
  new_password = dicted_data['new_password']
  user = db_session.query(User).filter(User.id == session['id']).first()
  if user and argon2.verify(password, user.password) == True:
    new_password_hash = argon2.hash(new_password)
    user.password = new_password_hash
    db_session.commit()
    #mail_passwd_update(user.mail, new_password)
    return "User updated successfully !"
  else:
    return "Bad Password, contact Admin if you forgot it"
  return "OK"

@app.route("/updateUser", methods=["POST"])
def update_user():
  expected = ('login', 'new_password')
  try:
    dicted_data = required_params_are_ok(request, expected)
    is_logged()
    is_admin()
  except ValueError as err:
    return str(err)

  login = dicted_data['login']
  new_password = dicted_data['new_password']
  user = db_session.query(User).filter(User.login == login).first()
  if user:
    new_password_hash = argon2.hash(new_password)
    user.password = new_password_hash
    db_session.commit()
    #mail_passwd_update(user.mail, new_password)
    return "User updated successfully !"
  else:
    return "Bad Password, contact Admin if you forgot it"
  return "OK"

@app.route("/users/<id_user>", methods=["DELETE"])
def users_del(id_user):
  try:
    is_logged()
    is_admin()
  except ValueError as err:
    return str(err)
  user = db_session.query(User).filter(User.id == id_user).first()
  if user:
    db_session.delete(user)
    db_session.commit()
    return "User deleted successfully"
  else:
    return "User not found"
  return "OK"


@app.route("/users/<login>", methods=["GET"])
def user_detail(login):
  user = db_session.query(User).filter(User.login == login).all()

  try:
    User.exists_and_is_unique(user)
    return jsonify(user_schema.dump(user[0]).data)
  except ValueError as err:
    return str(err)

