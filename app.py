from flask import Flask, render_template, request, redirect
import sqlite3
from pathlib import Path
app = Flask(__name__)

def get_db_connection():
    """
    Izveido un atgriež savienojumu ar SQLite datubāzi.
    """
    db = Path(__file__).parent / "receptes_database"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    conn = get_db_connection() 
    kategorijas = conn.execute("SELECT * FROM categories").fetchall()
    conn.close()
    return render_template("base.html", kategorijas=kategorijas)

@app.route("/category/<type2>")
def category(type2):
    conn = get_db_connection()

    receptes = conn.execute("""
        SELECT *
        FROM recipes
        JOIN categories ON recipes.category_id = categories.id
        WHERE categories.type2 = ?
    """, (type2,)).fetchall()

    conn.close()

    return render_template(
        "category.html",
        receptes=receptes
    )

@app.route("/recepte/<int:id>")
def recepte(id):
    conn = get_db_connection()

    recipe = conn.execute("""
        SELECT *
        FROM recipes
        JOIN categories ON recipes.category_id = categories.id
        WHERE recipes.id = ?
    """, (id,)).fetchone()

    ingredients = conn.execute("""
        SELECT *
        FROM ingredients
        WHERE recipe_id = ?
    """, (id,)).fetchall()

    comments = conn.execute("""
        SELECT *
        FROM comments
        WHERE recipe_id = ?
    """, (id,)).fetchall()

    conn.close()

    return render_template(
        "recepte.html",
        recipe=recipe,
        ingredients=ingredients,
        comments=comments
    )

@app.route("/comment/delete/<int:comment_id>", methods=["POST"])
def delete_comment(comment_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    conn.commit()
    conn.close()
    return redirect(request.referrer)

@app.route("/comment/update/<int:comment_id>", methods=["POST"])
def update_comment(comment_id):
    text = request.form["comment_text"]
    rating = request.form["rating"]

    conn = get_db_connection()
    conn.execute("""
        UPDATE comments
        SET comment_text = ?, rating = ?
        WHERE id = ?
    """, (text, rating, comment_id))

    conn.commit()
    conn.close()

    return redirect(request.referrer)

@app.route("/comment/create", methods=["POST"])
def create_comment():
    recipe_id = request.form["recipe_id"]
    user_id = request.form["user_id"]
    text = request.form["comment_text"]
    rating = request.form["rating"]

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO comments (recipe_id, user_id, comment_text, rating)
        VALUES (?, ?, ?, ?)
    """, (recipe_id, user_id, text, rating))

    conn.commit()
    conn.close()

    return redirect(f"/recepte/{recipe_id}")

@app.route('/par-mums')
def par():
    return render_template('par-mums.html')

if __name__ == "__main__":
    app.run(debug=True)