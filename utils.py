
from flask import session

def is_logged():
  if 'login' not in session:
    raise ValueError('User not logged')
  else:
    return True

def is_admin():
  if 'role' not in session or session['role'] != 'administrator':
    raise ValueError('Admin access required')
  else:
    return True

def required_params_are_ok(request, expected):
  to_return = {}
  if len(request.form) > 0:
    to_check = request.form
    for submitted in request.form:
      to_return[submitted] = request.form[submitted]
  else:
    to_check = request.json
    to_return = request.json
  if not all (k in to_check for k in expected):
    raise ValueError("Missing info : should furnish " + " ".join(expected))
  else:
    return to_return

