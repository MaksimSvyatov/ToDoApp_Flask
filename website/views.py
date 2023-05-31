from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Task, User#, Comment, Like
from . import db
from datetime import datetime
import time


views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
    tasks = Task.query.all()
    return render_template('home.html', user=current_user, tasks=tasks)

@views.route('/create-task', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        text = request.form.get('text')

        if not text:
            flash('Task cannot be empty', category='error')
        else:
            task = Task(text=text, author=current_user.id)
            db.session.add(task)
            db.session.commit()
            flash('Task created!', category='success')
        return redirect(url_for('views.home'))
    
    return render_template('create_task.html', user=current_user)

@views.route("/edit-task/<id>", methods=['POST', 'GET'])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    text = request.form.get('text')
    if request.method == 'POST':
        text = request.form.get('text')
        task = Task.query.get_or_404(id)
        text = request.form.get('text')
        task.text = text

        task.date_updated = datetime.now().replace(microsecond=0)
        # print(task.date_updated)

        db.session.add(task)
        db.session.commit()
        flash('Task updated!', category='success')

        return redirect(url_for('views.home'))
    
    return render_template('edit_task.html', user=current_user, text=task.text)

@views.route("/delete-task/<id>")
@login_required
def delete_task(id):
    task = Task.query.filter_by(id=id).first()

    if not task:
        flash("Task does not exist.", category='error')
    elif current_user.id != task.id:
        flash('You do not have permission to delete this task.', category='error')
    else:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted.', category='success')

    return redirect(url_for('views.home'))

@views.route("/tasks/<username>")
@login_required
def tasks(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    tasks = user.tasks
    return render_template("tasks.html", user=current_user, tasks=tasks, username=username)

# @views.route("/edit-task/<id>")
# @login_required
# def edit_task(id):
#     pass

# @views.route("/create-comment/<post_id>", methods=['POST'])
# @login_required
# def create_comment(post_id):
#     text = request.form.get('text')

#     if not text:
#         flash('Comment cannot be empty.', category='error')
#     else:
#         post = Post.query.filter_by(id=post_id)
#         if post:
#             comment = Comment(
#                 text=text, author=current_user.id, post_id=post_id)
#             db.session.add(comment)
#             db.session.commit()
#         else:
#             flash('Post does not exist.', category='error')

#     return redirect(url_for('views.home'))


# @views.route("/delete-comment/<comment_id>")
# @login_required
# def delete_comment(comment_id):
#     comment = Comment.query.filter_by(id=comment_id).first()

#     if not comment:
#         flash('Comment does not exist.', category='error')
#     elif current_user.id != comment.author and current_user.id != comment.post.author:
#         flash('You do not have permission to delete this comment.', category='error')
#     else:
#         db.session.delete(comment)
#         db.session.commit()

#     return redirect(url_for('views.home'))

# @views.route("/like-post/<post_id>", methods=['POST'])
# @login_required
# def like(post_id):
#     post = Post.query.filter_by(id=post_id).first()
#     like = Like.query.filter_by(
#         author=current_user.id, post_id=post_id).first()

#     if not post:
#         return jsonify({'error': 'Post does not exist.'}, 400)
#     elif like:
#         db.session.delete(like)
#         db.session.commit()
#     else:
#         like = Like(author=current_user.id, post_id=post_id)
#         db.session.add(like)
#         db.session.commit()

#     return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})