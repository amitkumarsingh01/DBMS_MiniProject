from flask import Flask, render_template, redirect, request, session, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    password = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    issue = db.Column(db.String(255), nullable=False)
    suggestion = db.Column(db.String(255))
    date = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(255))
    location = db.Column(db.String(100))
    status = db.Column(db.String(50), default="Pending")
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['password']
        user_type = request.form['user_type']
        new_user = User(email=email, name=name, phone=phone, password=password, user_type=user_type)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please login.")
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user_type = request.form['user_type']
    user = User.query.filter_by(email=email, password=password, user_type=user_type).first()
    if user:
        session['user_id'] = user.id
        session['user_type'] = user.user_type
        if user.user_type == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user.user_type == 'staff':
            return redirect(url_for('staff_dashboard'))
        elif user.user_type == 'user':
            return redirect(url_for('user_dashboard'))
    elif email == 'amit@gmail.com' and password == '12345':
        session['user_id'] = 0
        session['user_type'] = 'admin'
        return redirect(url_for('admin_dashboard'))
    flash("Invalid credentials. Please try again.")
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect(url_for('index'))



@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session or session['user_type'] != 'user':
        return redirect(url_for('index'))
    user_id = session['user_id']
    queries = Query.query.filter_by(user_id=user_id).all()
    return render_template('user_dashboard.html', queries=queries)

@app.route('/staff_dashboard')
def staff_dashboard():
    if 'user_id' not in session or session['user_type'] != 'staff':
        return redirect(url_for('index'))
    staff_id = session['user_id']
    queries = Query.query.filter_by(staff_id=staff_id).all()
    return render_template('staff_dashboard.html', queries=queries)

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('index'))
    users = User.query.filter_by(user_type='user').all()
    staff = User.query.filter_by(user_type='staff').all()
    queries = Query.query.all()
    return render_template('admin_dashboard.html', users=users, staff=staff, queries=queries)

@app.route('/submit_query', methods=['GET', 'POST'])
def submit_query():
    if 'user_id' not in session or session['user_type'] != 'user':
        return redirect(url_for('index'))
    if request.method == 'POST':
        user_id = session['user_id']
        department = request.form['department']
        issue = request.form['issue']
        suggestion = request.form['suggestion']
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        file = request.files['file']
        file_path = None
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = filename
        location = request.form['location']
        new_query = Query(user_id=user_id, department=department, issue=issue, suggestion=suggestion, date=date, file_path=file_path, location=location)
        db.session.add(new_query)
        db.session.commit()
        flash("Query submitted successfully!")
        return redirect(url_for('user_dashboard'))
    return render_template('query_form.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/allocate_work', methods=['POST'])
def allocate_work():
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('index'))
    query_id = request.form['query_id']
    staff_id = request.form['staff_id']
    query = Query.query.get(query_id)
    query.staff_id = staff_id
    query.status = "Assigned"
    db.session.commit()
    flash("Work allocated successfully!")
    return redirect(url_for('admin_dashboard'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
