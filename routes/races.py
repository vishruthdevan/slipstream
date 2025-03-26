from flask import g, render_template
from sqlalchemy import text

from routes import races_bp


@races_bp.route("/")
def races():
    """Retrieve and display races from the database."""
    query = text("SELECT raceid, name, date FROM race")
    cursor = g.conn.execute(query)

    races_data = []
    for row in cursor:
        races_data.append({"id": row[0], "name": row[1], "date": row[2]})
    cursor.close()

    return render_template("races.html", races=races_data)
