from flask import Flask, jsonify, request
from models import db, Book 

app = Flask(__name__)

# Konfigurasi database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Menginisialisasi db dengan aplikasi Flask
db.init_app(app)

# Tambahkan route untuk membuat tabel jika belum ada
@app.route('/create_db', methods=['GET'])
def create_db():
    with app.app_context():
        db.create_all()  # Membuat tabel berdasarkan model yang sudah didefinisikan
    return "Database and tables created!"


@app.route('/books', methods=['GET'])  # Perbaiki method menjadi methods
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@app.route('/books/<int:id>', methods=['GET'])  # Perbaiki method menjadi methods
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book.to_dict())

@app.route('/books', methods=['POST'])  
def add_book():
    data = request.get_json()
    new_book = Book(
        title=data['title'],
        author=data['author'],
        published_year=data['published_year']
    )

    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201

@app.route('/books/<int:id>', methods=['PUT']) 
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()

    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.published_year = data.get('published_year', book.published_year)

    db.session.commit()
    return jsonify(book.to_dict())


@app.route('/books/<int:id>', methods=['DELETE']) 
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Buku berhasil dihapus'}), 200

if __name__ == "__main__":
    app.run(debug=True)
