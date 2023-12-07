" routes.py file where all the routes are configured"

from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db, login_manager
from app.forms import LoginForm, SignupForm, EditUsernameForm, EditFontSizeForm, SearchForm, EditPasswordForm
from app.models import User, Post, Like
from sqlalchemy import or_

# login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# home
@app.route("/")
@login_required
def home():
    search_form = SearchForm()
    # Get posts from the current user and their followings
    user_ids_to_query = [user.id for user in current_user.following]
    # Include the current user's posts
    user_ids_to_query.append(current_user.id)
    all_posts = Post.query.filter(Post.user_id.in_(
        user_ids_to_query)).order_by(Post.date_posted.desc()).all()

    # Pass the liked status of each post to the template
    liked_posts = [post.has_user_liked(current_user) for post in all_posts]

    return render_template('home.html', posts=all_posts,
                           liked_posts=liked_posts, search_form=search_form)

# login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your username and password.',
                  'danger')

    return render_template('login.html', form=form)

# logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        # Check if the username already exists
        existing_user = User.query.filter_by(
            username=form.username.data).first()

        if existing_user:
            flash('Username already exists. Please choose a different username.',
                  'danger')
        else:
            # Create a new user if the username is unique and passwords match
            new_user = User(username=form.username.data, 
                            password=form.password.data)
            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully. You can now log in.',
                  'success')
            return redirect(url_for('signup'))

    # If there are form validation errors, flash all error messages
    for field, errors in form.errors.items():
        for field in errors:
            flash(f'{field}', 'danger')

    return render_template('signup.html', form=form)

# profile
@app.route('/profile')
@login_required
def profile():
    search_form = SearchForm() 
    return render_template('profile.html', search_form=search_form)

# edit username
@app.route('/edit_username', methods=['GET', 'POST'])
@login_required
def edit_username():
    form = EditUsernameForm()

    if form.validate_on_submit():
        # Check if the new username already exists
        existing_user = User.query.filter_by(
            username=form.new_username.data).first()

        if existing_user:
            flash('Username already exists. Please choose a different username.',
                  'danger')
        else:
            # Update the current user's username
            current_user.username = form.new_username.data
            db.session.commit()

            flash('Username updated successfully!', 'success')
            return redirect(url_for('profile'))

    return render_template('edit_username.html', form=form)

# other user profile
@app.route('/user/<username>')
@login_required
def other_user_profile(username):
    other_user = User.query.filter_by(username=username).first()
    search_form = SearchForm()

    # Get posts from the current user and their followings
    user_ids_to_query = [user.id for user in current_user.following]
    # Include the current user's posts
    user_ids_to_query.append(current_user.id)
    all_posts = Post.query.filter(Post.user_id.in_(
        user_ids_to_query)).order_by(Post.date_posted.desc()).all()

    # Pass the liked status of each post to the template
    liked_posts = [post.has_user_liked(current_user) for post in all_posts]

    if other_user:
        return render_template('other_user_profile.html',
                               other_user=other_user,
                               liked_posts=liked_posts,
                               search_form=search_form)
    else:
        abort(404)

# like post
@app.route('/like_post/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get(post_id)

    if post:
        if not post.has_user_liked(current_user):
            like = Like(user=current_user, post=post)
            db.session.add(like)
            db.session.commit()
        else:
            # Unlike the post
            like = Like.query.filter_by(user=current_user, post=post).first()
            db.session.delete(like)
            db.session.commit()

    return redirect(url_for('home'))

# explore
@app.route("/explore", methods=['GET', 'POST'])
@login_required
def explore():
    # Handle the search form
    search_form = SearchForm()

    if search_form.validate_on_submit():
        search_query = f"%{search_form.username.data}%"
        users = User.query.filter(or_(User.username.ilike(search_query),
                                      User.id.ilike(search_query))).all()
    else:
        # Display all users
        users = User.query.all()

    return render_template('explore.html', users=users,
                           search_form=search_form)

# follow
@app.route("/follow/<username>", methods=['POST'])
@login_required
def follow(username):
    user_to_follow = User.query.filter_by(username=username).first()

    if user_to_follow and current_user != user_to_follow:
        current_user.following.append(user_to_follow)
        db.session.commit()

    # Check the source of the follow action based on the referrer
    referrer = request.referrer
    explore_url = url_for('explore')
    home_url = url_for('home')

    if referrer and explore_url in referrer:
        return redirect(explore_url)
    elif referrer and home_url in referrer:
        return redirect(home_url)
    else:
        return redirect(url_for('profile'))

# unfollow
@app.route("/unfollow/<username>", methods=['POST'])
@login_required
def unfollow(username):
    user_to_unfollow = User.query.filter_by(username=username).first()

    if user_to_unfollow and current_user != user_to_unfollow:
        current_user.following.remove(user_to_unfollow)
        db.session.commit()

    # Check the source of the unfollow action based on the referrer
    referrer = request.referrer
    explore_url = url_for('explore')
    home_url = url_for('home')

    if referrer and explore_url in referrer:
        return redirect(explore_url)
    elif referrer and home_url in referrer:
        return redirect(home_url)
    else:
        return redirect(url_for('profile'))

# post create
@app.route('/post_create', methods=['POST'])
def post_create():
    if request.method == 'POST':
        content = request.form.get('content')

        # Create a new post
        new_post = Post(content=content, user=current_user)

        # Save the post to the database
        db.session.add(new_post)
        db.session.commit()

        # Redirect to the home page
        return redirect(url_for('home'))

    return redirect(url_for('home'))

# delete post
@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post_to_delete = Post.query.get(post_id)

    # Check if the post exists and if the current user
    # is the owner of the post
    if post_to_delete and post_to_delete.user == current_user:
        # Delete associated likes first
        likes_to_delete = Like.query.filter_by(post_id=post_id).all()
        for like in likes_to_delete:
            db.session.delete(like)

        # delete the post
        db.session.delete(post_to_delete)
        db.session.commit()

        flash('Post deleted successfully!', 'success')
    else:
        # abort if the post doesn't exist or the user is not the owner
        abort(403)

    return redirect(url_for('home'))

# edit post
@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post_to_edit = Post.query.get(post_id)

    # Check if the post exists and if the current user
    # is the owner of the post
    if post_to_edit and post_to_edit.user == current_user:
        if request.method == 'POST':
            # Update the post content
            post_to_edit.content = request.form.get('content')
            db.session.commit()

            flash('Post edited successfully!', 'success')

            # Check the source of the edit action based on the referrer
            referrer = request.referrer
            profile_url = url_for('profile')

            if referrer and profile_url in referrer:
                return redirect(profile_url)
            else:
                return redirect(url_for('home'))

        return render_template('edit_post.html', post=post_to_edit)

    abort(403)

# settings
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = EditFontSizeForm()

    if form.validate_on_submit():
        # Update the user's font size preference
        current_user.font_size = form.font_size.data
        db.session.commit()

        flash('Font size updated successfully!', 'success')
        return redirect(url_for('settings'))

    return render_template('settings.html', form=form)

# edit password
@app.route('/edit_password', methods=['GET', 'POST'])
@login_required
def edit_password():
    form = EditPasswordForm()

    if form.validate_on_submit():
        flash('Password changed successfully!', 'success')
        return redirect(url_for('settings'))
    else:
        # Flash validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{error}', 'danger')

        return render_template('edit_password.html', form=form)
