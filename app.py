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
    return render_template("index.html", kategorijas=kategorijas)

@app.route("/category/<type2>")
def category(type2):
    conn = get_db_connection() 
    receptes = conn.execute("""SELECT * FROM recipes, categories WHERE categories.type2 = ?""",(type2,),).fetchall()
    conn.close()
    return render_template(f"{type2}.html",  receptes=receptes)
    


if __name__ == "__main__":
    app.run(debug=True)