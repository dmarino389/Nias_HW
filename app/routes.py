from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import FamilyMember, User  # Import the User model
from app.forms import RegistrationForm, LoginForm, EditMemberForm  # Import your user input forms
from datetime import datetime
import csv
import smtplib
from email.mime.text import MIMEText
from io import StringIO

@app.route('/')
@login_required
def index():
    # Fetch only family members associated with the current user
    family_members = FamilyMember.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', family_members=family_members)

@app.route('/add_member', methods=['GET', 'POST'])
@login_required
def add_member():
    if request.method == 'POST':
        birthdate_str = request.form['birthdate']
        birthdate = datetime.strptime(birthdate_str, '%m-%d-%Y').date() if birthdate_str else None

        new_member = FamilyMember(
            user_id=current_user.id,  # Associate the new member with the current user
            name=request.form['name'],
            relationship=request.form['relationship'],
            address=request.form['address'],
            birthdate=birthdate,
            medical_records=request.form['medical_records'],
            notes=request.form['notes']
        )
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_member.html')

@app.route('/delete_member/<int:member_id>', methods=['POST'])
@login_required
def delete_member(member_id):
    member_to_delete = FamilyMember.query.get(member_id)
    if member_to_delete and member_to_delete.user_id == current_user.id:
        db.session.delete(member_to_delete)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/edit_member/<int:member_id>', methods=['GET', 'POST'])
@login_required
def edit_member(member_id):
    family_member = FamilyMember.query.get_or_404(member_id)

    if family_member.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('index'))

    form = EditMemberForm(obj=family_member)
    if form.validate_on_submit():
        form.populate_obj(family_member)
        db.session.commit()
        flash('Family member information has been updated.', 'success')
        return redirect(url_for('index'))

    return render_template('edit_member.html', form=form)

@app.route('/member/<int:member_id>')
@login_required
def member_detail(member_id):
    family_member = FamilyMember.query.get_or_404(member_id)

    if family_member.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('index'))

    return render_template('member_detail.html', family_member=family_member)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
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


