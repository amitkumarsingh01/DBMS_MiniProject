from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, QueryForm, FeedbackForm
from app.models import User, QueryForm as QueryModel, FeedbackForm as FeedbackModel
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, phone_number=form.phone_number.data, password=form.password.data, role='user')
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif current_user.role == 'staff':
        return redirect(url_for('staff_dashboard'))
    else:
        return redirect(url_for('user_dashboard'))

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    queries = QueryModel.query.all()
    return render_template('admin_dashboard.html', queries=queries)

@app.route('/user_dashboard')
@login_required
def user_dashboard():
    if current_user.role != 'user':
        return redirect(url_for('index'))
    queries = QueryModel.query.filter_by(user_id=current_user.id).all()
    return render_template('user_dashboard.html', queries=queries)

@app.route('/staff_dashboard')
@login_required
def staff_dashboard():
    if current_user.role != 'staff':
        return redirect(url_for('index'))
    queries = QueryModel.query.filter_by(status='Approved').all()
    return render_template('staff_dashboard.html', queries=queries)

@app.route('/query', methods=['GET', 'POST'])
@login_required
def query():
    form = QueryForm()
    if form.validate_on_submit():
        query = QueryModel(user_id=current_user.id, department=form.department.data, description=form.description.data, suggestion=form.suggestion.data, geolocation=form.geolocation.data)
        db.session.add(query)
        db.session.commit()
        flash('Your query has been submitted!', 'success')
        return redirect(url_for('user_dashboard'))
    return render_template('query_form.html', title='Submit Query', form=form)

@app.route('/feedback/<int:query_id>', methods=['GET', 'POST'])
@login_required
def feedback(query_id):
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = FeedbackModel(query_id=query_id, rating=form.rating.data, suggestion=form.suggestion.data)
        db.session.add(feedback)
        db.session.commit()
        flash('Your feedback has been submitted!', 'success')
        return redirect(url_for('user_dashboard'))
    return render_template('feedback_form.html', title='Submit Feedback', form=form)
