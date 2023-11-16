# routes.py
from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import FamilyMember




@app.route('/')
def index():
    family_members = FamilyMember.query.all()
    return render_template('index.html', family_members=family_members)

@app.route('/add_member', methods=['GET', 'POST'])
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
def delete_member(member_id):
    global family_members

    # Find and remove the member with the specified member_id
    family_members = [member for member in family_members if member["id"] != member_id]

    return redirect(url_for('index'))
