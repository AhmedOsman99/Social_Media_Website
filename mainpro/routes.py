from flask import render_template, redirect, url_for, flash, request, Blueprint
from mainpro import app, db, bcrypt
from mainpro.forms import RegistrationForm, LoginForm
from mainpro.models import User
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/login', methods=['GET','POST'])
def login():
    
    return render_template('login.html', data={'title':endpoint_title,'form':form})
