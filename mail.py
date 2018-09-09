from wgsi import app
from flask_mail import Mail, Message

app.config['MAIL_SERVER']='mail.pseudo.moi'
app.config['MAIL_PORT'] = 25

webmaster = 'webmaster@pseudo.moi'

mail = Mail(app)

def mail_login(receiver):
  msg = Message('Login Notification', sender = webmaster, recipients = [receiver])
  msg.body = "You've logged in ! Amazing info here"
  try:
    mail.send(msg)
  except:
    print 'error sending mail'
  return True

def mail_passwd_update(receiver, password):
  msg = Message('Password Notification', sender = webmaster, recipients = [receiver])
  msg.body = "Your password has been updated ! It is now {}".format(password)
  try:
    mail.send(msg)
  except:
    print 'error sending mail'
  return True

def mail_user_created(receiver, login, passwd):
  msg = Message('Account creation', sender = webmaster, recipients = [receiver])
  msg.body = "An account has been created for you, login = {}, passwd = {}, you can update your password by clicking on this link : youporn.com".format(login, passwd)
  try:
    mail.send(msg)
  except:
    print 'error sending mail'
  return True
