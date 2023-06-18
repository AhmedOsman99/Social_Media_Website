from flask import render_template, redirect, url_for, flash, request, Blueprint
from mainpro import app, db, bcrypt
from mainpro.forms import RegistrationForm, LoginForm
from mainpro.models import User, Friendshiprequest, Friendship
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.orm import aliased
from sqlalchemy import text

@app.route('/')
def main():
    return render_template('base.html')


@app.route('/home')
@login_required
def home():
    return render_template('home.html', data={})


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')
        
    form = LoginForm()
    if form.validate_on_submit():
        with app.app_context():
            target_user = User.query.filter_by(username=form.username.data).first()
            if target_user and bcrypt.check_password_hash(target_user.password, form.password.data):
                login_user(target_user)
                return redirect('home')
            
                
    return render_template('login.html', data={'form': form})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
    

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/home')

    form = RegistrationForm()
    if form.validate_on_submit():
        with app.app_context():    
            hashed_pass = bcrypt.generate_password_hash(form.password.data)
            register_user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_pass,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                middle_name=form.middle_name.data,
                birth_date=form.birth_date.data
            )
            db.session.add(register_user)
            db.session.commit()
        return redirect('login')
    return render_template('register.html', data={'form': form})


@app.route('/find_friends', methods=['GET', 'POST'])
@login_required
def find_friends():
    all_users = ""
    pending_user = db.session.query(
        Friendshiprequest,
        User
    )\
    .filter(Friendshiprequest.user_id == current_user.id)\
    .join(User, User.id == Friendshiprequest.friend_id).all()
    
    subquery1 = db.session.query(
        Friendship.friend_id
    )\
    .join(User, User.id == current_user.id)\
    .filter(Friendship.user_id == current_user.id)\
    .subquery()
    
    subquery2 = db.session.query(
        Friendshiprequest.friend_id
    )\
    .filter(Friendshiprequest.user_id == current_user.id)\
    .subquery()

    subquery3 = db.session.query(
        Friendshiprequest.user_id,
    )\
    .filter(Friendshiprequest.friend_id == current_user.id)\
    .join(User, User.id == Friendshiprequest.user_id)\
    .subquery()

    print(subquery3)

    not_friend_users = db.session.query(
        User
    )\
    .filter(User.id != current_user.id, ~User.id.in_(subquery1), ~User.id.in_(subquery2), ~User.id.in_(subquery3))\
    .all()

    return render_template('find_friends.html', data={'pending_user': pending_user, 'not_friend_users': not_friend_users})


@app.route('/find_friends/<user_id>', methods=['GET', 'POST'])
@login_required
def view_user_profile(user_id):
    with app.app_context():
        user = User.query.filter_by(id=user_id).first()
    return render_template('view_user_profile.html', data={'user': user})


@app.route('/send_request/<new_friend_id>', methods=['GET', 'POST'])
@login_required
def send_request(new_friend_id):
    with app.app_context():
        new_friend = db.session.query(
            User
        )\
        .filter(User.id == new_friend_id)\
        .first()
        new_request = Friendshiprequest(
            user_id = current_user.id,
            friend_id = new_friend_id,
            status = "Pending"
        )
        db.session.add(new_request)
        new_friend.pendings = new_friend.pendings + 1
        db.session.commit()
    return redirect('/find_friends')
        

@app.route('/friend_requests', methods=['GET', 'POST'])
@login_required
def friend_requests():
    user_requests = db.session.query(
        Friendshiprequest,
        User
    )\
    .filter(Friendshiprequest.friend_id == current_user.id)\
    .join(User, User.id == Friendshiprequest.user_id).all()
    return render_template('friend_requests.html', data={'user_requests': user_requests})


@app.route('/friend_requests_accept/<friendID>', methods=['GET', 'POST'])
@login_required
def accept_friend_request(friendID):
    added_user = db.session.query(
        User
    )\
    .filter(User.id == friendID).first()
    with app.app_context():
        new_friendship_1 = Friendship(
            user_id = current_user.id,
            friend_id = friendID
        )
        new_friendship_2 = Friendship(
            user_id = friendID,
            friend_id = current_user.id
        )

        accepted_request = db.session.query(
            Friendshiprequest
        )\
        .filter(Friendshiprequest.user_id == added_user.id)\
        .filter(Friendshiprequest.friend_id == current_user.id)\
        .first()

        current_user.pendings = current_user.pendings - 1
        current_user.no_of_friends = current_user.no_of_friends + 1
        added_user.no_of_friends = added_user.no_of_friends + 1

        db.session.add(new_friendship_1)
        db.session.add(new_friendship_2)
        db.session.delete(accepted_request)
        db.session.commit()

    flash(f'{added_user.first_name} is now your friend!', 'success') 
    return redirect('/friend_requests')


@app.route('/friend_requests_decline/<friendID>', methods=['GET', 'POST'])
@login_required
def decline_friend_request(friendID):
    added_user = db.session.query(
        User
    )\
    .filter(User.id == friendID)\
    .first()
    with app.app_context():
        accepted_request = db.session.query(
            Friendshiprequest
        )\
        .filter(Friendshiprequest.user_id == added_user.id)\
        .filter(Friendshiprequest.friend_id == current_user.id)\
        .first()
        db.session.delete(accepted_request)

        current_user.pendings = current_user.pendings - 1

        db.session.commit()

    flash(f"You just declined {added_user.first_name}'s request", 'info') 
    return redirect('/friend_requests')
        

@app.route('/my_friends', methods=['GET', 'POST'])
@login_required
def my_friends():
    with app.app_context():
        friends = db.session.query(
            Friendship,
            User
        )\
        .filter(Friendship.user_id == current_user.id)\
        .join(User, User.id == Friendship.friend_id).all()
        print(friends)

    return render_template('my_friends.html', data={'friends': friends } )


@app.route('/remove_friend/<friendID>', methods=['GET', 'POST'])
@login_required
def remove_friend(friendID):
    removed_friend = db.session.query(
        User
    )\
    .filter(User.id == friendID).first()
    with app.app_context():
        remove_query_1 = db.session.query(
            Friendship
        )\
        .filter(Friendship.user_id == removed_friend.id, Friendship.friend_id == current_user.id)\
        .first()
        remove_query_2 = db.session.query(
            Friendship
        )\
        .filter(Friendship.user_id == current_user.id, Friendship.friend_id == removed_friend.id)\
        .first()
        db.session.delete(remove_query_1)
        db.session.delete(remove_query_2)
        current_user.no_of_friends = current_user.no_of_friends - 1
        removed_friend.no_of_friends = removed_friend.no_of_friends - 1

        db.session.commit()

    flash(f"You removed {removed_friend.first_name} from your friends!", "info")
    return redirect('/my_friends')


@app.route('/cancel_request/<friendID>', methods=['GET', 'POST'])
@login_required
def cancel_request(friendID):
    with app.app_context():
        request = db.session.query(
            Friendshiprequest
        )\
        .filter(Friendshiprequest.user_id == current_user.id, Friendshiprequest.friend_id == friendID)\
        .first()
        requested_friend = db.session.query(
            User
        )\
        .filter(User.id == friendID)\
        .first()
        requested_friend.pendings = requested_friend.pendings - 1 
        db.session.delete(request)
        db.session.commit()
    return redirect('/find_friends')