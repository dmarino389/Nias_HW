from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from app.forms import RegistrationForm, LoginForm, EditMemberForm  # Import your user input forms
from datetime import datetime
from app.models import User, FamilyMember  # Import your database models

@app.route('/')
@login_required
def index():
    
    return render_template('index.html')

@app.route('/add_member', methods=['GET', 'POST'])
@login_required
def add_member():
    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('add_member.html')

@app.route('/delete_member/<int:member_id>', methods=['POST'])
@login_required
def delete_member(member_id):
    return redirect(url_for('index'))

@app.route('/edit_member/<int:member_id>', methods=['GET', 'POST'])
@login_required
def edit_member(member_id):
    form = EditMemberForm()
    if form.validate_on_submit():
        flash('Family member information has been updated.', 'success')
        return redirect(url_for('index'))

    return render_template('edit_member.html', form=form)

@app.route('/member/<int:member_id>')
@login_required
def member_detail(member_id):
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))