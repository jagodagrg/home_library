from flask import Flask, request, render_template, redirect, url_for
from models import books, BookForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "lalala"


@app.route("/books/", methods=["GET", "POST"])
def books_list():
    form = BookForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            books.create(form.data)
            books.save_all()
        return redirect(url_for("books_list"))
    return render_template("books.html", form=form, books=books.all(), error=error)


@app.route("/books/<int:book_id>/", methods=["GET", "POST"])
def book_details(book_id):
    book = books.get(book_id - 1)
    form = BookForm(data=book)
    if request.method == "POST":
        if form.validate_on_submit():
            books.update(book_id - 1, form.data)
        return redirect(url_for("books_list"))
    if request.method == "DELETE":
        books.delete(book_id)
        books.save_all()
        return redirect(url_for("books_list"))
    return render_template("book.html", form=form, book_id=book_id)


@app.route("/books/to_be_sold", methods=["GET"])
def to_be_sold():
    form = BookForm()
    error = ""
    return render_template("to_be_sold.html", form=form, books=books.show_to_be_sold(), error=error)


@app.route("/books/unread", methods=["GET"])
def unread():
    form = BookForm()
    error = ""
    return render_template("unread.html", form=form, books=books.show_unread(), error=error)


if __name__ == "__main__":
    app.run(debug=True)
