from flask import g, render_template
from sqlalchemy import text

from routes import constructors_bp


@constructors_bp.route("/<int:constructor_id>/")
def constructor_detail(constructor_id):
    """Retrieve and display details for a specific constructor."""
    query = text(
        "SELECT constructorid, name, nationality FROM constructor WHERE constructorid = :constructor_id"
    )
    cursor = g.conn.execute(query, {"constructor_id": constructor_id})

    constructor_data = cursor.fetchone()
    cursor.close()

    if constructor_data:
        return render_template("constructor_detail.html", constructor=constructor_data)
    return render_template("not_found.html"), 404


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
