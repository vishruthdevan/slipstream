from flask import g, render_template
from sqlalchemy import text

from routes import sprint_results_bp  # Ensure this Blueprint is registered


@sprint_results_bp.route("/<int:race_id>/")
def sprint_results(race_id):
    """Retrieve and display details for a specific sprint race."""
    query = text(
        """
        SELECT sr.position, sr.points, 
        d.driverid, d.firstname, d.lastname, 
        c.constructorid, c.name as constructor_name, r.name AS race_name, r.date
        FROM sprintresults sr
        JOIN race r ON sr.raceid = r.raceid AND r.raceid = :race_id
        JOIN driver d ON sr.driverid = d.driverid
        JOIN constructor c ON sr.constructorid = c.constructorid
        ORDER BY sr.position ASC
        """
    )

    cursor = g.conn.execute(query, {"race_id": race_id})
    sprint_results_data = []

    for row in cursor:
        sprint_results_data.append(
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

    if sprint_results_data:
        return render_template(
            "sprint_results.html", sprint_results=sprint_results_data
        )
    return render_template("not_found.html"), 404
