from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['MONGO_URI'] ="mongodb+srv://vrushti9421:UFNmPIfd92HNW9PR@cluster0pt.jzcfs46.mongodb.net/chatgpt"
mongo = MongoClient(app.config['MONGO_URI'])
db = mongo.get_database()

login_manager = LoginManager(app)

# Replace this with your user model
class User:
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    # Replace this with the logic to load the user from your database
    # Example: return User(user_id)
    pass

@app.route('/')
def index():
    notes = db.notes.find({'user_id': current_user.id})
    return render_template('index.html', notes=notes)

@app.route('/add-note', methods=['POST'])
def add_note():
    note_data = request.form['note']
    db.notes.insert_one({'user_id': current_user.id, 'note': note_data})
    return jsonify({'message': 'Note added successfully'})

@app.route('/delete-note', methods=['POST'])
def delete_note():
    note_id = request.json['noteId']
    note = db.notes.find_one({'_id': note_id, 'user_id': current_user.id})
    if note:
        db.notes.delete_one({'_id': note_id})
        return jsonify({'message': 'Note deleted successfully'})
    else:
        return jsonify({'message': 'Note not found or unauthorized'}), 403

if __name__ == '__main__':
    app.run(debug=True)
