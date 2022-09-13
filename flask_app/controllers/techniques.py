from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.technique import Technique

@app.route('/newtip')
def add_technique():
    data={
        'user_id':session['user_id']
    }
    if not data:
        redirect('index.html')
    else:
        return render_template('addtip.html')

@app.route('/add/tip', methods=['POST'])
def post_new_tip():
    data={
        'name': request.form['name'],
        'type': request.form['type'],
        'comments': request.form['comments'],
        'rating': request.form['rating'],
        'user_id': session['user_id'],
    }

    Technique.add_tip(data)
    print(data)
    return redirect ('/dashboard')

@app.route('/viewuser/')
@app.route('/viewuser')
def view_profile():
    data={
        'user_id':session['user_id']
    }
    tips = Technique.posted_by_user(data)
    # user=User.get_one_with_tips(data)
    return render_template('userinfo.html', tips = tips, orange='orange')