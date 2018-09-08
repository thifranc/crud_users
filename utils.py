
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

def required_params_are_ok(expected, request):
  if not all (k in request for k in expected):
    raise ValueError("Missing info : should furnish " + " ".join(expected))
  else:
    return True

