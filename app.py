from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_pymongo import PyMongo
from bson import ObjectId
from flask_bcrypt import Bcrypt
import os
import re

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")  
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
mongo = PyMongo(app)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate email syntax
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return 'Invalid email syntax'

        user = mongo.db.users.find_one({'email': email})

        if user and bcrypt.check_password_hash(user['password'], password):
            # Set session
            session['user'] = {'email': user['email']}
            return redirect(url_for('notes'))
        else:
            return 'Invalid email or password'

    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate email syntax
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return 'Invalid email syntax'

        # Check if the email already exists in the database
        existing_user = mongo.db.users.find_one({'email': email})

        if existing_user:
            return 'Email already exists'
        else:
            # Hash the password and store the user in the database
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user_data = {'email': email, 'password': hashed_password}
            mongo.db.users.insert_one(user_data)

            # Set session
            session['user'] = {'email': email}
            return redirect(url_for('notes'))

    return render_template("register.html")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/get_note_data', methods=['POST'])
def get_note_data():
    title = request.form.get('title')
    note_data = mongo.db.notes.find_one({'title': title})

    # Convert ObjectId to string before jsonify
    if note_data and '_id' in note_data:
        note_data['_id'] = str(note_data['_id'])

    return jsonify(note_data)

@app.route('/delete_note', methods=['POST'])
def delete_note():
        title = request.form.get('title')

        # Delete the note from MongoDB
        result = mongo.db.notes.delete_one({'title': title})

        if result.deleted_count > 0:
            return jsonify({'message': 'Note deleted successfully'})
        else:
            return jsonify({'message': 'Note not found or could not be deleted'})
    
@app.route('/edit_note', methods=['POST'])
def edit_note():
      title = request.form.get('title')
      description = request.form.get('description')
  
      # Update the note in MongoDB
      result = mongo.db.notes.update_one(
          {'title': title},
          {'$set': {'description': description}}
      )
  
      if result.modified_count > 0:
          return jsonify({'message': 'Note updated successfully'})
      else:
          return jsonify({'message': 'Note not found or could not be updated'})
  

# Flask route to get user email
@app.route('/get_user_email', methods=['GET'])
def get_user_email():
    user_email = session.get('user', {}).get('email', '')
    return jsonify({'email': user_email})



@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        # Get the current user's email from the session
        user_email = session.get('user', {}).get('email')

        # Insert the note into MongoDB with the user's email
        note_data = {'title': title, 'description': description, 'user_email': user_email}
        mongo.db.notes.insert_one(note_data)

    # Get the current user's email from the session
    user_email = session.get('user', {}).get('email')

    # Fetch notes associated with the current user
    notes = mongo.db.notes.find({'user_email': user_email})
    myNotes = [note for note in notes]

    return render_template("notes.html", myNotes=myNotes)

# ...











