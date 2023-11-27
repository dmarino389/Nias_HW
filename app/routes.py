from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import FamilyMember, User  # Import the User model
from app.forms import RegistrationForm, LoginForm, EditMemberForm  # Import your user input forms

# Remove the global family_members list

@app.route('/')
@login_required
def index():
    family_members = FamilyMember.query.all()
    return render_template('index.html', family_members=family_members)

@app.route('/add_member', methods=['GET', 'POST'])
@login_required
def add_member():
    if request.method == 'POST':
        new_member = FamilyMember(
            name=request.form['name'],
            relationship=request.form['relationship'],
            address=request.form['address'],
            medical_records=request.form['medical_records']
        )
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_member.html')

@app.route('/delete_member/<int:member_id>', methods=['POST'])
@login_required
def delete_member(member_id):
    # Find and delete the member with the specified member_id from the database
    member_to_delete = FamilyMember.query.get(member_id)

    if member_to_delete:
        db.session.delete(member_to_delete)
        db.session.commit()

    return redirect(url_for('index'))

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


@app.route('/edit_member/<int:member_id>', methods=['GET', 'POST'])
@login_required  # Ensure that the user is logged in to access this route
def edit_member(member_id):
    # Retrieve the family member to be edited
    family_member = FamilyMember.query.get(member_id)

    if not family_member:
        flash('Family member not found.', 'danger')
        return redirect(url_for('index'))

    form = EditMemberForm(obj=family_member)

    if form.validate_on_submit():
        # Update the family member's information
        form.populate_obj(family_member)
        db.session.commit()
        flash('Family member information has been updated.', 'success')
        return redirect(url_for('index'))

    return render_template('edit_member.html', form=form)

