# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_bootstrap import Bootstrap
from models import db, Todo
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
# Bootstrap(app)
db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    if task:
        new_todo = Todo(task=task)
        db.session.add(new_todo)
        db.session.commit()
        flash('Tugas berhasil ditambahkan!', 'success')
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_todo(id):
    todo = Todo.query.get_or_404(id)
    if request.method == 'POST':
        todo.task = request.form.get('task')
        todo.status = 'status' in request.form
        db.session.commit()
        flash('Tugas berhasil diperbarui!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', todo=todo)

@app.route('/delete/<int:id>')
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    flash('Tugas berhasil dihapus!', 'success')
    return redirect(url_for('index'))

@app.route('/toggle_status/<int:id>')
def toggle_status(id):
    todo = Todo.query.get_or_404(id)
    todo.status = not todo.status  # Toggle status
    db.session.commit()
    flash('Status tugas berhasil diubah!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)