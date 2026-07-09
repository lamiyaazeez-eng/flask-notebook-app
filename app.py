from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)
NOTES_FILE = 'notes.json'

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r') as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
    return []

def save_notes(notes):
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f,indent=2)

notes = load_notes()
next_id = max([note['id'] for note in notes], default=0) + 1

@app.route('/')
def home():
    return render_template('index.html', notes=notes, error=None)

@app.route('/add', methods=['POST'])
def add_note():
    global next_id
    note = request.form.get('note','').strip()
    color = request.form.get('color', '#fffdf9')  # Default color is white
    error = None
    if note:
        notes.append({'id': next_id, 'content': note, 'pinned': False, 'timestamp':datetime.now().strftime('%Y-%m-%d %H:%M:%S') ,'color': color})
        next_id += 1
        save_notes(notes)
        return redirect(url_for('home'))
    else:
        return render_template('index.html', notes=notes, error="Note content cannot be empty.")

@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    global notes
    notes = [note for note in notes if note['id'] != note_id]
    save_notes(notes)
    return render_template('index.html', notes=notes)   

@app.route('/pin/<int:note_id>')
def pin_note(note_id):
    for note in notes:
        if note['id'] == note_id:
            note['pinned'] = not note['pinned']
    save_notes(notes)   
    return render_template('index.html', notes=notes)

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note_to_edit = next((n for n in notes if n['id'] == note_id), None)
    if request.method == 'POST':
        new_content = request.form.get('note')
        if note_to_edit and new_content:
            note_to_edit['content'] = new_content
        return render_template('index.html', notes=notes)
    return render_template('edit.html', note=note_to_edit)

if __name__ == '__main__':
    app.run(debug=True)