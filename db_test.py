from mainpro import db, app
from mainpro.models import User, Post, Friendship
import sys

def create_db():
    with app.app_context():
        db.create_all()

def drop_dp():
    with app.app_context():
        db.drop_all()


# create
def create_user():
    with app.app_context():
        new_user = User(username="amr", email='amr.3brazek@gmail.com', password='123')
        db.session.add(new_user)
        db.session.commit()

def create_post():
    with app.app_context():
        user = User.query.first()
        post_1 = Post(title="test", content='test content', user_id = user.id)
        post_1 = Post(title="test2", content='test content2', user_id = user.id)
        db.session.add(post_1)
        db.session.commit()

def create_friendship():
    with app.app_context():
        new_friendship = Friendship(user_id = 18 , friend_id = 12)
        new_friendship2 = Friendship(user_id = 12 , friend_id = 18)
        db.session.add(new_friendship)
        db.session.add(new_friendship2)
        db.session.commit()


# read 
def read_user():
    with app.app_context():
        user = User.query.first()
        # print(f"user is {user}")
        print(f"user is {user.username}")
        for post in user.posts:
            print(f"post is {post.title} content: {post.content}")

        users = User.query.all()
        for user in users:
            print(user)
        
        users=User.query.filtr_by(password='123').all()
        users=User.query.filtr_by(password='123').first()

        query = db.session.query(
            Post,
            User
        )\
        .join( User, Post.user_id == User.id)\
        .filter(Post.title == 'test title 1')\
        .order_by(Post.id.desc())\
        .all()

        for item in query:
            print (item.Post)
            print (item.User.username)

def update_users():
    with app.app_context():
        user = User.query.filter()
        print(user)
        user.email = 'xyz@gmail.com'
        db.session.commit()
        user = User.query.filter()
        print(user)

def delete_posts():
    with app.app_context():
        post = Post.query.first()
        print(post)
        db.session.delete(post)
        db.session.commit()
        post = Post.query.first()
        print(post)


if __name__ == '__main__':
    globals()[sys.argv[1]]()