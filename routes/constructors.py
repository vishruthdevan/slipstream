from flask import g, render_template
from sqlalchemy import text

from routes import constructors_bp


@constructors_bp.route("/")
def constructors():
    """Retrieve and display constructors from the database."""
    query = text("SELECT constructorid, name, nationality FROM constructor")
    cursor = g.conn.execute(query)

    constructors_data = []
    for row in cursor:
        constructors_data.append({"id": row[0], "name": row[1], "nationality": row[2]})
    cursor.close()

    return render_template("constructors.html", constructors=constructors_data)
