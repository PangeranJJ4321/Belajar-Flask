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
    search_query = request.args.get("search", "").strip().lower()

    if search_query:
        todos = Todo.query.filter(Todo.task.ilike(f"%{search_query}%")).all()
    else:
        todos = Todo.query.all()

    page = request.args.get("page", 1, type=int)  # Ambil nomor halaman dari URL
    per_page = 5  # Jumlah tugas per halaman
    total_todos = len(todos)  # Total jumlah tugas
    start = (page - 1) * per_page
    end = start + per_page
    paginated_todos = todos[start:end]  # Ambil tugas berdasarkan halaman
    
    total_pages = (total_todos + per_page - 1) // per_page  # Hitung jumlah halaman

    return render_template(
        'index.html', 
        todos=paginated_todos,
        search_query=search_query,
        page=page,
        total_pages=total_pages  # Ubah total_todos menjadi total_pages
    )

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