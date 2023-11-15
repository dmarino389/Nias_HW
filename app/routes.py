from flask import Flask, render_template, request, redirect, url_for, jsonify
from app import app, db
from app.models import FamilyMember

@app.route('/')
def index():
    # Example of how you might organize your family members
    family_tree = {
        'grandparents': FamilyMember.query.filter_by(relationship='grandparent').order_by(FamilyMember.birthdate).all(),
        'parents': FamilyMember.query.filter_by(relationship='parent').order_by(FamilyMember.birthdate).all(),
        'children': FamilyMember.query.filter_by(relationship='child').order_by(FamilyMember.birthdate).all(),
        # Add more relationships as needed
    }
    return render_template('index.html', family_tree=family_tree)




@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        # Extract form data and create a new FamilyMember instance
        new_member = FamilyMember(
            name=request.form['name'],
            relationship=request.form['relationship'],
            address=request.form['address'],  # Assuming you've added this in your model
            medical_records=request.form['medical_records']  # Assuming you've added this in your model
        )
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_member.html')


# Route to display details of a family member
@app.route('/member/<int:member_id>')
def member_details(member_id):
    member = FamilyMember.query.get_or_404(member_id)
    return jsonify({
        'name': member.name,
        'relationship': member.relationship,
        'address': member.address,
        'medical_records': member.medical_records
    })

# Route to delete a family member
@app.route('/delete_member/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    member = FamilyMember.query.get_or_404(member_id)
    db.session.delete(member)
    db.session.commit()
    return redirect(url_for('index'))

# Route to update a family member's information
@app.route('/update_member/<int:member_id>', methods=['GET', 'POST'])
def update_member(member_id):
    member = FamilyMember.query.get_or_404(member_id)
    if request.method == 'POST':
        member.name = request.form['name']
        member.relationship = request.form['relationship']
        member.address = request.form['address']
        member.medical_records = request.form['medical_records']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_member.html', member=member)

