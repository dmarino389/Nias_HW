from flask import Flask, render_template, request, redirect, url_for
from app import app


# Initialize an empty list to store family history records
family_history = []

@app.route('/')
def index():
    # You can add any data you want to pass to the template here
    return render_template('index.html')



# Function to add a new family history record
@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        # Process form data and add a new record to family_history
        # ...
        return redirect(url_for('add_record'))  # Redirect to the add_record page after submission
    return render_template('add_record.html')

# Function to search for family history records
@app.route('/search_records', methods=['GET', 'POST'])
def search_records():
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        results = []
        # Implement search logic and populate 'results' list
        # ...
        return render_template('search_results.html', results=results)
    return render_template('search_records.html')

# Function to display all family history records
@app.route('/display_records')
def display_records():
    return render_template('display_records.html', family_history=family_history)
