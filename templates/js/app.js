// app.js

function addNote() {
    const noteText = document.getElementById('new-note').value;

    fetch("/add-note", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `note=${encodeURIComponent(noteText)}`,
    })
    .then(() => {
        fetchNotes();
    });
}

function deleteNote(noteId) {
    fetch("/delete-note", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ noteId: noteId }),
    })
    .then((_res) => {
        fetchNotes();
    });
}

function fetchNotes() {
    fetch("/get-notes")
    .then(response => response.json())
    .then(notes => {
        const notesContainer = document.getElementById('notes-container');
        notesContainer.innerHTML = '';

        notes.forEach(note => {
            const noteElement = document.createElement('div');
            noteElement.className = 'note';
            noteElement.innerHTML = `
                <p>${note.note}</p>
                <button onclick="deleteNote('${note._id}')">Delete</button>
            `;
            notesContainer.appendChild(noteElement);
        });
    });
}

// Fetch notes when the page loads
document.addEventListener('DOMContentLoaded', fetchNotes);
