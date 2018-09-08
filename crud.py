from flask import Flask, request, jsonify, session
from model import User, UserSchema, RoleSchema, Session
from passlib.hash import argon2
from marshmallow import pprint
from utils import is_logged, is_admin, required_params_are_ok

import json


from wgsi import app

db_session = Session()

user_schema = UserSchema(only=('id', 'login', 'role', 'mail'))
users_schema = UserSchema(only=('id', 'login', 'role', 'mail'), many=True)
roles_schema = RoleSchema(many=True)

@app.route('/')
def hello_world():
  print session
  if 'login' not in session:
    return "You should get logged in my bro"
  else:
    if 'role' not in session:
      return "Somthg is wrong with your session"
    elif session['role'] == 'administrator':
      return "You are administator waow"
    elif session ['role'] == 'default':
      return "You are basic"
    else:
      return 'Hello, World!'

@app.route('/login', methods=['POST'])
def login():
  expected = ('login', 'password')
  try:
    required_params_are_ok(request.json, expected)
  except ValueError as err:
    return str(err)

  login = request.json['login']
  password = request.json['password']

  if 'login' in session:
    return 'Already logged in !'

  user = db_session.query(User).filter(User.login == login).first()
  if argon2.verify(password, user.password) == True:
    session['login'] = user.login
    session['id'] = user.id
    session['role'] = user.role.name
    return 'Session initiated {}'.format(session)
  else:
    return 'No session'


@app.route("/users", methods=["POST"])
def add_user():
  expected = ('login', 'password', 'id_role', 'mail')
  print expected
  try:
    required_params_are_ok(request.json, expected)
    is_logged()
    is_admin()
  except ValueError as err:
    return str(err)

  login = request.json['login']
  mail = request.json['mail']
  password = argon2.hash(request.json['password'])
  id_role = request.json['id_role']

  user = db_session.query(User).filter(User.login == login).all()

  if len(user) != 0:
    return "Login already taken"

  new_user = User(login, password, id_role, mail)

  db_session.add(new_user)
  db_session.commit()
  db_session.refresh(new_user)

  epure = user_schema.dumps(new_user)
  return jsonify(epure.data)


@app.route("/users", methods=["GET"])
def get_user():
  all_users = db_session.query(User).all()
  result = users_schema.dumps(all_users)
  return jsonify(result.data)


@app.route("/users/<login>", methods=["GET"])
def user_detail(login):
  user = db_session.query(User).filter(User.login == login).all()

  print len(user)
  try:
    User.exists_and_is_unique(user)
    print user_schema.dump(user[0])
    return jsonify(user_schema.dump(user[0]).data)
  except ValueError as err:
    return err


#@app.route("/users/<username>", methods=["PUT", "PATCH"])
#def user_update(username):
#  user = User.query.filter(User.username == username).all()
#
#  try:
#    User.exists_and_is_unique(user)
#  except ValueError as err:
#    return err
#
#  username = request.json['username'] if 'username' in request.json else None
#  value = request.json['value'] if 'value' in request.json else None
#
#  user = user[0]
#  if value:
#    user.value = value
#  if username:
#    user.username = username
#
#  db_session.commit()
#  return user_schema.jsonify(user)
#
#@app.route("/users/<username>", methods=["DELETE"])
#def user_delete(username):
#  user = User.query.filter(User.username == username).all()
#
#  if User.handle_error_db(user) is not None:
#    return User.handle_error_db(user)
#  user = user[0]
#
#  db_session.delete(user)
#  db_session.commit()
#
#  return user_schema.jsonify(user)
#


