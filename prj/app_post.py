from flask import redirect, render_template, request, jsonify, Blueprint, session, g, url_for
from models import User, Post, db
import datetime
from datetime import timezone


board = Blueprint('post', __name__)


@board.before_app_request
def load_logged_in_user():
    username = session.get('login')
    if username is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.username == username).first()


@board.route("/blog", methods=["GET"])
def forum():
    post_list = Post.query.order_by(Post.created_at.desc())

    return render_template('blog.html', post_list=post_list)


@board.route("/post", methods=["GET", "POST"])
def post():
    # 로그인하지 않은 상태일 때
    if session['login'] == None:
        return render_template('login.html', message="You need to login first.")

    # 로그인 한 상태일 때    
    else:
        # 글 작성 후 폼 제출시 db에 커밋 ("POST")
        if request.method == "POST":
            title = request.form['title']
            author = session['login']
            content = request.form['content']
            created_at = datetime.datetime.now(timezone.utc)
            print(title, author, content, created_at)

            new_post = Post(title, author, content, created_at)
            db.session.add(new_post)
            db.session.commit()
            return render_template('blog.html', message="Submitted.")

        # 링크로 접근시 작성 폼 ("GET")
        else:
            return render_template('post.html')

@board.route('/edit', methods=["GET","POST"])



@board.route("/content/<int:postid>/", methods=["GET"])
def show_post(postid):
    if session['login']:
        post = Post.query.get(postid)
        return render_template('content.html', post=post)
    else:
        return render_template('login.html', message="You need to login to see this post.")

@board.route('/')