from flask import Flask, jsonify, abort, make_response, request, render_template
from models import books

app = Flask(__name__)
app.config["SECRET_KEY"] = "tralala"


@app.route("/api/v1/books/", methods=['GET'])
def books_list_api_v1():
    return jsonify(books.all())


@app.route("/api/v1/books/", methods=['POST'])
def create_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    book = {
        'id': books.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'author': request.json['author'],
        'notes': request.json.get('notes', ""),
        'read': request.json['read'],
        'to_be_kept': request.json['to_be_kept']
    }
    books.create(book)
    return jsonify({'book': book}), 201


@app.route("/api/v1/books/<int:book_id>", methods=['GET'])
def get_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    return jsonify({"book": book})


@app.route("/api/v1/books/<int:book_id>", methods=['DELETE'])
def delete_book(book_id):
    result = books.delete(book_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/v1/books/<int:book_id>", methods=['PUT'])
def update_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'author' in data and not isinstance(data.get('author'), str),
        'notes' in data and not isinstance(data.get('notes'), str),
        'read' in data and not isinstance(data.get('read'), bool),
        'to_be_kept' in data and not isinstance(data.get('to_be_kept'), bool)
    ]):
        abort(400)
    book = {
        'id': data.get('id', book['id']),
        'title': data.get('title', book['title']),
        'author': data.get('author', book['author']),
        'notes': data.get('notes', book['notes']),
        'read': data.get('read', book['read']),
        'to_be_kept': data.get('to_be_kept', book['to_be_kept'])
    }
    books.update(book_id, book)
    return jsonify({'book': book})


@app.route("/api/v1/books/<int:book_id>", methods=['POST'])
def copy_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if all([
        'title' in data and isinstance(data.get('title'), str),
        'author' in data and isinstance(data.get('author'), str),
        'notes' in data and isinstance(data.get('notes'), str),
        'read' in data and isinstance(data.get('read'), bool),
        'to_be_kept' in data and isinstance(data.get('to_be_kept'), bool)
    ]):
        book = {
            'id': books.all()[-1]['id'] + 1,
            'title': data.get('title', book['title']),
            'author': data.get('author', book['author']),
            'notes': 'DUPLICATE',
            'read': data.get('read', book['read']),
            'to_be_kept': False
        }
        books.create(book)
        return jsonify({'book': book}), 201
    else:
        abort(400)


@app.route("/api/v1/books/to_be_sold", methods=['GET'])
def to_be_sold():
    return jsonify(books.show_to_be_sold())


@app.route("/api/v1/books/unread", methods=['GET'])
def unread():
    return jsonify(books.show_unread())


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


if __name__ == "__main__":
    app.run(debug=True)
