from flask import Flask, request, jsonify
from model import User, UserSchema, RoleSchema, Session
from passlib.hash import argon2
from marshmallow import pprint


#from wgsi import app
app = Flask(__name__)


session = Session()

user_schema = UserSchema(only=('login', 'id_role'))
users_schema = UserSchema(only=('login', 'id_role'), many=True)
roles_schema = RoleSchema(many=True)

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route("/users", methods=["POST"])
def add_user():
  if not all (k in request.json for k in ('login', 'password', 'id_role')):
    return "Missing info : should furnish login, password, id_role"

  login = request.json['login']
  password = argon2.hash(request.json['password'])
  id_role = request.json['id_role']

  user = session.query(User).filter(User.login == login).all()
  if len(user) != 0:
    return "Login already taken"

  print user

  new_user = User(login, password, id_role)

  print new_user

  session.add(new_user)
  session.commit()
  session.refresh(new_user)

  epure = user_schema.dumps(new_user)
  return jsonify(epure)

@app.route("/users", methods=["GET"])
def get_user():
  all_users = User.query.all()
  result = users_schema.dump(all_users)
  return jsonify(result.data)


@app.route("/users/<login>", methods=["GET"])
def user_detail(login):
  user = session.query.filter(User.login == login).all()

  try:
    User.exists_and_is_unique(user)
    return user_schema.jsonify(user[0])
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
#  session.commit()
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
#  session.delete(user)
#  session.commit()
#
#  return user_schema.jsonify(user)
#


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


