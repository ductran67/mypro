import mysql.connector, re
from config import MySQLDatabase
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def index():
  db = MySQLDatabase('config.json')
  db.connect()
  # db.call_stp_test('GetUserNameStp')
  user_list = db.call_stp('GetUserNameStp', None, "resultset")
  db.close()
  return render_template('index.html', user_list = user_list)

@app.route('/register')
def register():
  return render_template('register.html')

@app.route('/adduser', methods=['POST'])
def user():
  # Getting fields' values from Registration form
  username = request.form['username']
  password = request.form['password']
  confirm_password = request.form['confirm_password']
  nickname = request.form['nickname']
  email = request.form['email']
  # usertype = 2 for normal user, usertype = 1 for admin
  usertype = 2
  note = ''
  if password == confirm_password:
    db = MySQLDatabase('config.json')
    db.connect()
    existing_user = db.call_stp('CheckExistUserStp',(username,0), "output_params")
    if existing_user[1] > 0:
      print('Username already exists.')
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
      print('Invalid email address.')
    else:
      args = (username,password,nickname,email,usertype,note,"","",0)
      userid = db.call_stp('InsUserStp', args, "output_params")
      db.close()
      print(f'Registration successful! UserId = {userid}')
      return redirect(url_for('index'))
    db.close()
    return redirect(url_for('register'))
  else:
    print('Passwords do not match. Please try again.')
    return redirect(url_for('register'))

if __name__ == '__main__':
  app.run(debug=True)
