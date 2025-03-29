from flask import g, render_template
from sqlalchemy import text

from routes import constructor_standings_bp


@constructor_standings_bp.route("/")
def constructor_standings():
    """Retrieve and display current standings."""
    query = text(
        "SELECT cs.constructorid, c.name, cs.points, cs.rank FROM constructorstandings cs JOIN constructor c ON cs.constructorid = c.constructorid ORDER BY cs.points DESC"
    )

    cursor = g.conn.execute(query)

    standings_data = []
    for row in cursor:
        standings_data.append(
            {"constructor_id": f"{row[0]}", "name": f"{row[1]}", "points": row[2]}
        )
    cursor.close()

    return render_template("constructor_standings.html", standings=standings_data)
