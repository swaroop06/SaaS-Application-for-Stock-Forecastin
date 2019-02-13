from flask import Flask, request, render_template, flash, session, redirect, url_for
app = Flask(__name__,template_folder='template')
import os
@app.route('/', methods=['GET','POST'])
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('dashboard.html')


@app.route('/dashboard',methods=['GET','POST'])
def login():
    if request.form['username'] != 'admin' or \
        request.form['password'] != 'admin':
        error = 'Invalid username or password. Please try again!'
    else:
        flash('You were successfully logged in')
        return render_template('dashboard.html')
    return render_template('login.html', error = error)

@app.route('/home', methods=['GET','POST'])
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    return render_template('register.html')

@app.route('/registration', methods=['GET','POST'])
def registration():
    if len(request.form) < 2:
        error = 'Name too short'
        return render_template('register.html',error=error)
    if request.form['password'] != request.form['confirmpassword']:
        error = 'Passwords do not match'
        return render_template('register.html',error=error)
    error = 'Registration Successful! Please Login'    
    return render_template('register.html',error=error)



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)    