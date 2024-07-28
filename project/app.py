from flask import Flask, render_template, redirect, url_for, request, session
from models import db, User, Query, Feedback
from forms import LoginForm, RegisterForm, QueryForm, FeedbackForm
from utils import login_required, admin_required, staff_required

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['user_role'] = user.role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'staff':
                return redirect(url_for('staff_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    queries = Query.query.all()
    feedbacks = Feedback.query.all()
    return render_template('admin_dashboard.html', queries=queries, feedbacks=feedbacks)

@app.route('/staff/dashboard')
@staff_required
def staff_dashboard():
    queries = Query.query.filter_by(status='approved').all()
    return render_template('staff_dashboard.html', queries=queries)

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    user_id = session.get('user_id')
    queries = Query.query.filter_by(user_id=user_id).all()
    return render_template('user_dashboard.html', queries=queries)

@app.route('/query', methods=['GET', 'POST'])
@login_required
def query_form():
    form = QueryForm()
    if form.validate_on_submit():
        query = Query(
            user_id=session.get('user_id'),
            department=form.department.data,
            description=form.description.data,
            date=form.date.data,
            suggestion=form.suggestion.data,
            image=form.image.data,
            geolocation=form.geolocation.data
        )
        db.session.add(query)
        db.session.commit()
        return redirect(url_for('user_dashboard'))
    return render_template('query_form.html', form=form)

@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback_form():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(
            user_id=session.get('user_id'),
            query_id=form.query_id.data,
            rating=form.rating.data,
            suggestion=form.suggestion.data
        )
        db.session.add(feedback)
        db.session.commit()
        return redirect(url_for('user_dashboard'))
    return render_template('feedback_form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
