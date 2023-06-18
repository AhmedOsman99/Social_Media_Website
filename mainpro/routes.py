from flask import render_template, redirect, url_for, flash, request, Blueprint
from mainpro import app, db, bcrypt
from mainpro.forms import RegistrationForm, LoginForm
from mainpro.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os


@app.route('/register', methods=['GET','POST'])
def register():
    endpoint_title = "Register Page"
    form = RegistrationForm()
    if form.validate_on_submit():
        with app.app_context():
            profile_image=form.profile_image.data
            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(
                first_name=form.first_name.data,
                middle_name=form.middle_name.data,
                last_name=form.last_name.data,
                birth_date=form.birth_date.data,

                profile_image_data = profile_image.read(),
                profile_image_filename = profile_image.filename,

                username=form.username.data,
                email=form.email.data,
                password=hashed_pw
            )
            db.session.add(new_user)
            db.session.commit()

        file = form.profile_image.data # First grab the file
        filename = secure_filename(file.filename)
        file.seek(0)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filename)) # Then save the file


            # Save the uploaded image
        # return redirect(url_for('home'))
        return redirect(url_for('login'))
    # else:
            # return "dsa"
    #     flash("Registration Unsuccessful","danger")
    return render_template('register.html', data={'title':endpoint_title,'form':form})


@app.route('/login', methods=['GET','POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    endpoint_title = "Login Page"
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(url_for(next_page))
            else:
                # return redirect(url_for('home'))
                return "das"
        else:
            flash("Login Unsuccessful. Please check email and password.", "danger")
    return render_template('login.html', data={'title': endpoint_title, 'form': form})



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    