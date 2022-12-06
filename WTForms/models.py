import json
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    id = StringField('id', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    notes = StringField('notes')
    read = BooleanField('read')
    to_be_kept = BooleanField('to_be_kept')


class Books:
    def __init__(self):
        try:
            with open("books.json", "r") as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = []

    def all(self):
        return self.books

    def get(self, id):
        return self.books[id]

    def create(self, data):
        data.pop('csrf_token')
        self.books.append(data)

    def save_all(self):
        with open("books.json", "w") as f:
            json.dump(self.books, f, indent=4, separators=(". ", " = "))

    def update(self, id, data):
        data.pop('csrf_token')
        self.books[id] = data
        self.save_all()

    def show_to_be_sold(self):
        self.to_be_sold = [book for book in self.all() if not book['to_be_kept']]
        return self.to_be_sold

    def show_unread(self):
        self.unread = [book for book in self.all() if not book['read']]
        return self.unread


books = Books()
