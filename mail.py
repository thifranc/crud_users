from wgsi import app
from flask_mail import Mail, Message

app.config['MAIL_SERVER']='mail.pseudo.moi'
app.config['MAIL_PORT'] = 25
#app.config['MAIL_USERNAME'] = 'webmaster@pseudo.moi'
#app.config['MAIL_PASSWORD'] = '*****'
#app.config['MAIL_USE_TLS'] = False
#app.config['MAIL_USE_SSL'] = True

webmaster = 'webmaster@pseudo.moi'

mail = Mail(app)

def mail_login(receiver):
  msg = Message('Login Notification', sender = webmaster, recipients = [receiver])
  msg.body = "You've logged in ! Amazing info here"
  mail.send(msg)
  return True

def mail_passwd_update(receiver):
  msg = Message('Password Notification', sender = webmaster, recipients = [receiver])
  msg.body = "Your password has been updated !"
  mail.send(msg)
  return True

def mail_user_created(receiver, login, passwd):
  msg = Message('Account creation', sender = webmaster, recipients = [receiver])
  msg.body = "An account has been created for you, login = {}, passwd = {}, you can update your password by clicking on this link : youporn.com".format(login, passwd)
  mail.send(msg)
  return True
