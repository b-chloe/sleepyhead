from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.technique import Technique

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if User not in session:
        return render_template('index.html')
    else:
        return redirect('/dashboard')

@app.route('/register', methods=['POST'])
def register():
    is_valid = User.validate_user(request.form)
    if not is_valid:
        return redirect('/')
    else:
        new_user = {
            'fname': request.form['fname'],
            'email':request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        id = User.create_user(new_user)
        if not id:
            flash('Something went wrong!')
            return redirect('/')
        else :
            session['user_id'] = id
            flash("User registration successful!")
            return redirect ('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data={
        'email':request.form['email']
    }
    user = User.get_by_email(data)
    if not user:
        flash("We don't know that email. Register below instead!")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Wrong Password! Try Again.")
        return redirect ('/')
    else:
        session['user_id'] = user.id
        print("THIS SHOULD BE THE ID======>", user.id)
        flash('Welcome Back!')
        return redirect ('/dashboard')

@app.route('/dashboard')
def dash():
    data={
        'user_id':session['user_id']
    }
    all_tips = Technique.get_all_tips()
    # users= User.one_user(data)
    return render_template('dashboard.html', all_tips=all_tips)

# @app.route('/viewprofile/')
# @app.route('/viewprofile')
# def user_info():
#     data={
#         'user_id':session['user_id']
#     }
#     tips = Technique.posted_by_user(data)
#     # user=User.get_one_with_tips(data)
#     return render_template('profile.html', tips = tips, orange='orange')

# @app.route('/viewuser')
# def view_profile():
#     data={
#         'user_id':session['user_id']
#     }
#     tips = Technique.posted_by_user(data)
#     # user=User.get_one_with_tips(data)
#     return render_template('userinfo.html', tips = tips, orange='orange')

@app.route('/logout')
def logout():
    session.clear()
    flash("Bye!")
    return redirect('/')