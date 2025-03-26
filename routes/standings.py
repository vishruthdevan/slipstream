from flask import g, render_template
from sqlalchemy import text

from routes import standings_bp


@standings_bp.route("/")
def standings():
    """Retrieve and display current standings."""
    query = text(
        """
        SELECT driver.firstname, driver.lastname, seasonstandings.points, year 
        FROM seasonstandings 
        JOIN driver ON seasonstandings.driverid = driver.driverid
        ORDER BY seasonstandings.points DESC
        LIMIT 100;
    """
    )
    cursor = g.conn.execute(query)

    standings_data = []
    for row in cursor:
        standings_data.append({"name": f"{row[0]} {row[1]}", "points": row[2]})
    cursor.close()

    return render_template("standings.html", standings=standings_data)
