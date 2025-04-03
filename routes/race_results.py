from flask import g, render_template
from sqlalchemy import text

from routes import race_results_bp


@race_results_bp.route("/<int:race_id>/")
def race_results(race_id):
    """Retrieve and display details for a specific race."""
    query = text(
        """
        SELECT rr.position, rr.points, d.driverid, d.firstname, d.lastname, c.constructorid, c.name as constructor_name, r.name AS race_name, r.date
        FROM raceresults rr
        JOIN race r ON rr.raceid = r.raceid AND r.raceid = :race_id
        JOIN driver d ON rr.driverid = d.driverid
        JOIN constructor c ON rr.constructorid = c.constructorid
        ORDER BY rr.position ASC
    """
    )

    cursor = g.conn.execute(query, {"race_id": race_id})
    race_results_data = []

    for row in cursor:
        race_results_data.append(
            {
                "position": row[0],
                "points": row[1],
                "driver_id": row[2],
                "first_name": row[3],
                "last_name": row[4],
                "constructor_id": row[5],
                "constructor_name": row[6],
                "race_name": row[7],
                "date": row[8],
            }
        )
    cursor.close()

    if race_results_data is not None:
        return render_template("race_results.html", race_results=race_results_data)
    return render_template("not_found.html"), 404
