from flask import Flask, render_template, redirect, request, flash, session
import datetime
import re

app = Flask(__name__)
app.secret_key = 'thissecret'

num = re.compile('[0-9]')
upper = re.compile('[A-Z]')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


@app.route('/')
def index():
    print datetime.date.today()
    if ('error' not in session):
        session['error'] = False

    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    session['error'] = False
    dob = datetime.datetime.strptime

    if(len(request.form['email']) == 0):
        flash("Email can't be empty", "error")
        session['error'] = True

    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email", 'error')
        session['error'] = True

    if (len(request.form['first_name']) == 0):
        flash("First Name can't be empty", 'error')
        session['error'] = True
    else:
        if(num.search(request.form['first_name']) != None):
            flash("First name can't have numbers", 'error')
            session['error'] = True

    if (len(request.form['last_name']) == 0):
        flash("Last Name can't be empty", 'error')
        session['error'] = True

    else:
        if(num.search(request.form['last_name']) != None):
            flash("Last name can't have numbers", 'error')
            session['error'] = True


    if (len(request.form['password']) < 8):
        flash("Password must be 8 or more characters", 'error')
        session['error'] = True

    elif (num.search(request.form['password']) == None):
            flash("Password must have at least 1 number", 'error')
            session['error'] = True

    elif (upper.search(request.form['password']) ==  None):
        flash("Password must have at least 1 upper case letter", 'error')
        session['error'] = True

    if (request.form['password_confirm'] != request.form['password']):
        flash("Passords do not match", 'error')
        session['error'] = True

    try:
        dob(request.form['dob'], "%m/%d/%Y")
        if dob(request.form['dob'], "%m/%d/%Y") >= datetime.datetime.today():
            flash("Birthday invalid", 'error')
            session['error'] = True
    except:
        flash("Birthday invalid", 'error')
        session['error'] = True

    if (session['error'] == False):
        flash("Success! Thanks for submitting your information", 'success')

    return redirect('/')

app.run(debug=True)
