from flask import render_template, redirect, url_for, flash, request, Blueprint, send_from_directory
from mainpro import  app, bcrypt, db
from mainpro.models import User, Post, Friendship
from mainpro.forms import PostForm, RegistrationForm, LoginForm, EditForm
from flask import render_template, redirect, url_for, flash, request, Blueprint
from mainpro import app, db, bcrypt
from mainpro.forms import RegistrationForm, LoginForm
from mainpro.models import User, Friendshiprequest, Friendship
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os

from datetime import date


@app.route('/register', methods=['GET','POST'])
def register():
    endpoint_title = "Register Page"
    form = RegistrationForm()
    if form.validate_on_submit():
        with app.app_context():
            profile_image=form.profile_image.data
            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            profile_image_data = ""
            profile_image_filename = ""
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
            print(profile_image_data)
            print(profile_image_filename)
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

@app.route('/')
def main():
    return render_template('base.html', data={})



@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
                return redirect('home')
        else:
            flash("Login Unsuccessful. Please check email and password.", "danger")
    return render_template('login.html', data={'title': endpoint_title, 'form': form})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


Navbar = ['home', 'profile', "friends" , 'logout']

# delete post
@app.route('/home/<post_id>', methods=['GET','POST'])
@login_required
def delete_Post(post_id):

    with app.app_context():

        post_to_delete = Post.query.filter(Post.id == post_id).first()
        print("===========================================")
        print(post_to_delete)
        db.session.delete(post_to_delete)
        db.session.commit()

    flash("Post deleted", "success")
    return redirect(url_for('home'))
    

# home page & add post & edit post
@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
@app.route('/edit/<post_id>', methods = ['GET', 'POST'])
@login_required
def home(post_id = ""):
    
    form2 = None
    # edit post
    post_to_edit = None
    if post_id :
        # print("true")
        # post_to_edit = Post.query.filter_by(id == post_id).first()
        post_to_edit = db.session.query(
            Post,
        )\
        .filter(Post.id == post_id)\
        .first()


        if post_to_edit :
            print("true")
            form2 = PostForm(obj=post_to_edit)
            # print(form2)
            if form2.validate_on_submit():
                form2.populate_obj(post_to_edit)
                print("true2")
                if form2.post_image.data :
                    post_imagex = form2.post_image.data
                    post_image_data = post_imagex.read()
                    post_image_filename = post_imagex.filename
                else: 
                    post_image_data = post_to_edit.post_image_data
                    post_image_filename =  post_to_edit.post_image_filename

                with app.app_context():
                    form2.populate_obj(post_to_edit)
                    post_to_edit = Post.query.filter(Post.id == post_id).first()

                    post_to_edit.title = form2.title.data
                    post_to_edit.content = form2.content.data
                    post_to_edit.status = form2.status.data
                    post_to_edit.post_image_data = post_image_data
                    post_to_edit.post_image_filename = post_image_filename
                    db.session.commit()

                if form2.post_image.data :
                    file = form2.post_image.data # First grab the file
                    filename = secure_filename(file.filename)
                    file.seek(0)
                    file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filename)) # Then save the file

                    
                flash("Post updated Successful", "success")
                return redirect(url_for('home'))
        else:
            return "post doesn't exist"

    # add post
    form = PostForm()
    if form.validate_on_submit():
        print("valid")
        with app.app_context():

            # checking if there is an image uploaded
            if form.post_image.data :
                post_imagex = form.post_image.data
                post_image_data = post_imagex.read()
                post_image_filename = post_imagex.filename
            else: 
                post_image_data = b''
                post_image_filename =""

            new_post = Post(title=form.title.data,
                            content=form.content.data,
                            status=form.status.data,
                            user_id=current_user.id,
                            post_image_data = post_image_data,
                            post_image_filename = post_image_filename,
                            )
            db.session.add(new_post)
            db.session.commit()
        
        # upload the image if uloaded 
        if form.post_image.data :
            file = form.post_image.data # First grab the file
            filename = secure_filename(file.filename)
            file.seek(0)
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filename)) # Then save the file

        flash("Post added Successful", "success")
        return redirect(url_for('home'))
    

    friend_posts = []
    friendships = Friendship.query.filter((Friendship.user_id == current_user.id)).all()
    for friendship in friendships:
        friend_posts += User.query.get(friendship.friend_id).posts
        # friend_id = friendship.friend_id if friendship.user_id == user_id else friendship.user_id

    # Getting posts' ids for my friends 
    friends_posts  = list(filter(lambda post : post.status == 'Friends_only' , friend_posts ))
    posts_id = []
    for post in friends_posts:
        posts_id.append(post.id)

    friends_posts = list(filter(lambda post : post.status == 'Public' , friend_posts ))
    for post in friends_posts:
        posts_id.append(post.id)

    posts_onlyme = db.session.query(
            Post,
            User
        )\
        .join( User, Post.user_id == User.id)\
        .filter(Post.user_id == current_user.id)\
        .order_by(Post.date.desc())\
        .all()
    
    friendsandI_posts = db.session.query(
            Post,
            User
        )\
        .join( User, Post.user_id == User.id)\
        .filter(Post.id.in_(posts_id))\
        .order_by(Post.date.desc())\
        .all()
    
    posts_public = db.session.query(
            Post,
            User
        )\
        .join( User, Post.user_id == User.id)\
        .filter((Post.status == "Public") | (Post.user_id == current_user.id) | (Post.id.in_(posts_id)))\
        .order_by(Post.date.desc())\
        .all()

    endpoint_title = 'home'
    return render_template('home.html', data={ 'title':endpoint_title, 'Navbar':Navbar, 'form': form, "form2":form2, "user": current_user,  "posts_onlyme": posts_onlyme, "posts_public":posts_public, "friends_only_posts":friendsandI_posts, "friends_only_posts_ids":posts_id, 'post_to_edit':post_to_edit })

    

# about page
@app.route('/about')
@login_required
def about():
    endpoint_title = 'about'
    return render_template('about.html', data={ 'title':endpoint_title, 'Navbar':Navbar})



@app.route('/profile/<userID>')
@login_required
def profile(userID):
    # image = current_user.image.decode('utf-8')
    # print(current_user.image)
    today = date.today()
    born = current_user.birth_date
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    endpoint_title = 'profile'

    
    my_posts = Post.query.filter_by(user_id=userID).all()
    state = ""
    user = ""
    user = User.query.filter_by(id=userID).first()
    # print('test')
    # with app.app_context():
    #     if userID == current_user.id:
    #         user = current_user
    #     else:
    #         check_if_friend = db.session.query(Friendship.friend_id).filter(Friendship.user_id == current_user.id,
    #                                                                         Friendship.friend_id == userID).first()
    #         print(check_if_friend)
            
    #         check_if_pending = db.session.query(Friendshiprequest.user_id).filter(Friendshiprequest.user_id == current_user.id,
    #                                                                             Friendshiprequest.friend_id == userID).first()
    #         print(check_if_pending)
    #         if check_if_friend:
    #             state = 'friend'
    #             # user = User.query.filter_by(id=check_if_friend[0]).first()
    #         elif check_if_pending:
    #             state = 'pending'
    #             # user = User.query.filter_by(id=check_if_pending[0]).first()
    return render_template('profile.html', data={ 'title':endpoint_title, 'Navbar':Navbar, 'user': user, 'age': age,
    'my_posts': my_posts, 'state': state })




@app.route('/find_friends', methods=['GET', 'POST'])
@login_required
def find_friends():
    all_users = ""
    with app.app_context():
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
    
    
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in
def edit_profile():
    endpoint_title = "Edit Profile"
    form = EditForm(obj=current_user)

    if form.validate_on_submit():
        form.populate_obj(current_user)
        if form.profile_image.data:
            profile_imagex = form.profile_image.data
            profile_image_data = profile_imagex.read()
            profile_image_filename = profile_imagex.filename
        else: 
            profile_image_data = current_user.profile_image_data
            profile_image_filename =  current_user.profile_image_filename


        with app.app_context():
            form.populate_obj(current_user)
            current_user.first_name = form.first_name.data
            current_user.middle_name = form.middle_name.data
            current_user.last_name = form.last_name.data
            current_user.birth_date = form.birth_date.data
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.profile_image_data = profile_image_data
            current_user.profile_image_filename = profile_image_filename
            # curre.current_profile_image.data = current_user.profile_image_filename
            db.session.commit()

        if form.profile_image.data:
            # Check if a new profile image was uploaded
            file = form.profile_image.data # First grab the file
            filename = secure_filename(file.filename)
            file.seek(0)
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filename)) # Then save the file

            # db.session.commit()
        flash("Your profile has been updated successfully.", "success")
        return redirect(url_for('profile'))

    # Pre-fill the form with the current user's information
    # form.first_name.data = current_user.first_name
    # form.middle_name.data = current_user.middle_name
    # form.last_name.data = current_user.last_name
    # form.birth_date.data = current_user.birth_date
    # form.username.data = current_user.username
    # form.email.data = current_user.email

    return render_template('edit_profile.html', data={'title': endpoint_title, 'form': form})


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
    with app.app_context():
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
    with app.app_context():
        added_user = db.session.query(
            User
        )\
        .filter(User.id == friendID).first()
        print(added_user.no_of_friends)
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

        curr_user = db.session.query(User).filter(User.id == current_user.id).first()
        print(current_user.username)
        curr_user.pendings = curr_user.pendings - 1
        curr_user.no_of_friends = curr_user.no_of_friends + 1

        print(added_user.no_of_friends)
        added_user.no_of_friends = added_user.no_of_friends + 1

        print(added_user.username)

        print(added_user.no_of_friends)

        db.session.add(new_friendship_1)
        db.session.add(new_friendship_2)
        db.session.delete(accepted_request)
        db.session.commit()
        print("--------------------------------")

        print(added_user.no_of_friends)

        flash(f'{added_user.first_name} is now your friend!', 'success') 
        return redirect('/friend_requests')


@app.route('/friend_requests_decline/<friendID>', methods=['GET', 'POST'])
@login_required
def decline_friend_request(friendID):
    with app.app_context():
        added_user = db.session.query(
            User
        )\
        .filter(User.id == friendID)\
        .first()
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
    with app.app_context():
        removed_friend = db.session.query(
            User
        )\
        .filter(User.id == friendID).first()
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
        current_user.no_of_friends = current_user.no_of_friends - 1
        removed_friend.no_of_friends = removed_friend.no_of_friends - 1
        db.session.delete(remove_query_1)
        db.session.delete(remove_query_2)

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