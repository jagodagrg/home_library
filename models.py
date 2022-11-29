import json


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
        book = [book for book in self.all() if book['id'] == id]
        if book:
            return book[0]
        return []

    def create(self, data):
        self.books.append(data)
        self.save_all()

    def save_all(self):
        with open("books.json", "w") as f:
            json.dump(self.books, f)

    def update(self, id, data):
        book = self.get(id)
        if book:
            index = self.books.index(book)
            self.books[index] = data
            self.save_all()
            return True
        return False

    def delete(self, id):
        book = self.get(id)
        if book:
            self.books.remove(book)
            self.save_all()
            return True
        return False

    def show_to_be_sold(self):
        self.to_be_sold = []
        [self.to_be_sold.append(book) for book in self.all()
         if book['to_be_kept'] == False]
        return self.to_be_sold

    def show_unread(self):
        self.unread = []
        [self.unread.append(book) for book in self.all()
         if book['read'] == False]
        return self.unread


books = Books()
