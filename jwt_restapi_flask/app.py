from flask import Flask, jsonify, request
from dotenv import load_dotenv
from models import db, User, Book
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

# Load .env
load_dotenv()

app = Flask(__name__)

# Load konfigurasi dari environment variables dengan prefix FLASK_
app.config.from_prefixed_env()
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)



@app.route('/create_db')
def create():
    with app.app_context():  # Pastikan ada konteks aplikasi Flask
        db.create_all()
    return "<p>Berhasil dibut</p>"

# Endpoint untuk register
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Cek apakah username sudah ada di database
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'message': 'Username sudah digunakan!'}), 400  # Status 400: Bad Request
    
    # Jika belum ada, buat user baru
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User berhasil didaftarkan!'}), 201

# Endpoint untuk login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.username)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Username atau password salah'}), 401

# Endpoint untuk mendapatkan semua buku (butuh autentikasi JWT)
@app.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

# Endpoint lainnya tetap sama, hanya ditambahkan @jwt_required()
@app.route('/books/<int:id>', methods=['GET'])
@jwt_required()
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'message': f'Buku dengan ID {id} tidak ditemukan'}), 404
    
    return jsonify(book.to_dict()), 200


@app.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], published_year=data['published_year'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201

@app.route('/books/<int:id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.published_year = data.get('published_year', book.published_year)
    db.session.commit()
    return jsonify(book.to_dict())

@app.route('/books/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Buku berhasil dihapus'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)