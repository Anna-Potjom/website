from flask import Flask, render_template
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
        receptes=receptes,
    )

@app.route("/recepte/<int:id>")
def recepte(id):
    conn = get_db_connection()

    # get ONE recipe
    recipe = conn.execute("""
        SELECT *
        FROM recipes
        JOIN categories ON recipes.category_id = categories.id
        WHERE recipes.id = ?
    """, (id,)).fetchone()

    # get ingredients ONLY for this recipe
    ingredients = conn.execute("""
        SELECT *
        FROM ingredients
        WHERE recipe_id = ?
    """, (id,)).fetchall()

    conn.close()

    return render_template(
        "recepte.html",
        recipe=recipe,
        ingredients=ingredients
    )
    

if __name__ == "__main__":
    app.run(debug=True)