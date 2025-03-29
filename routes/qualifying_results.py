from flask import g, render_template
from sqlalchemy import text

from routes import qualifying_results_bp  # Ensure this Blueprint is registered


@qualifying_results_bp.route("/<int:race_id>/")
def qualifying_results(race_id):
    """Retrieve and display details for a specific qualifying session."""
    query = text(
        """
        SELECT q.position, q.q1, q.q2, q.q3, 
               d.firstname, d.lastname, 
               c.name AS constructor_name, 
               r.name AS race_name, r.date
        FROM qualifyingresults q
        JOIN race r ON q.raceid = r.raceid AND r.raceid = :race_id
        JOIN driver d ON q.driverid = d.driverid
        JOIN constructor c ON q.constructorid = c.constructorid
        ORDER BY q.position ASC
        """
    )

    cursor = g.conn.execute(query, {"race_id": race_id})
    qualifying_results_data = []

    for row in cursor:
        qualifying_results_data.append(
            {
                "position": row[0],
                "q1": row[1],
                "q2": row[2],
                "q3": row[3],
                "first_name": row[4],
                "last_name": row[5],
                "constructor_name": row[6],
                "race_name": row[7],
                "date": row[8],
            }
        )
    cursor.close()

    if qualifying_results_data:
        return render_template(
            "qualifying_results.html", qualifying_results=qualifying_results_data
        )
    return render_template("not_found.html"), 404
