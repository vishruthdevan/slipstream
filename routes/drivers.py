from flask import g, render_template
from sqlalchemy import text

from routes import drivers_bp


@drivers_bp.route("/")
def drivers():
    """Retrieve and display drivers from the database."""
    query = text("SELECT driverid, firstname, lastname, nationality FROM driver")
    cursor = g.conn.execute(query)

    drivers_data = []
    for row in cursor:
        drivers_data.append(
            {"id": row[0], "name": f"{row[1]} {row[2]}", "nationality": row[3]}
        )
    cursor.close()

    return render_template("drivers.html", drivers=drivers_data)
