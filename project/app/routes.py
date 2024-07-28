from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import os

from app import app, db
from app.forms import LoginForm, RegistrationForm, QueryForm, FeedbackForm
from app.models import User, Query, Feedback

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        if user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user.role == 'staff':
            return redirect(url_for('staff_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, phone_number=form.phone_number.data,
                    role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    queries = Query.query.all()  # Query database for all queries
    return render_template('admin_dashboard.html', queries=queries)

@app.route('/staff/dashboard')
@login_required
def staff_dashboard():
    if current_user.role != 'staff':
        return redirect(url_for('index'))
    queries = Query.query.filter_by(assigned_to=current_user.id).all()  # Query database for staff-specific queries
    return render_template('staff_dashboard.html', queries=queries)

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    if current_user.role != 'user':
        return redirect(url_for('index'))
    queries = Query.query.filter_by(user_id=current_user.id).all()  # Query database for queries submitted by the user
    return render_template('user_dashboard.html', queries=queries)

@app.route('/query', methods=['GET', 'POST'])
@login_required
def query():
    form = QueryForm()
    if form.validate_on_submit():
        filename = None
        if form.image_file.data:
            filename = secure_filename(form.image_file.data.filename)
            form.image_file.data.save(os.path.join('path/to/upload/directory', filename))
        # Save the query details to the database including the filename if applicable
        flash('Your query has been submitted', 'success')
        return redirect(url_for('user_dashboard'))
    return render_template('query_form.html', title='Submit Query', form=form)

@app.route('/feedback/<int:query_id>', methods=['GET', 'POST'])
@login_required
def feedback(query_id):
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(query_id=query_id, rating=form.rating.data, suggestion=form.suggestion.data)
        db.session.add(feedback)
        db.session.commit()
        flash('Your feedback has been submitted.')
        return redirect(url_for('user_dashboard'))
    return render_template('feedback_form.html', title='Give Feedback', form=form)
