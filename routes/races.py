from flask import g, render_template
from sqlalchemy import text

from routes import races_bp


@races_bp.route("/<int:race_id>/")
def race_detail(race_id):
    """Retrieve and display details for a specific race."""
    query = text(
        """
        SELECT r.raceid, r.name, r.year, r.round, r.date, r.time, r.weather, r.circuitid,
               c.name AS circuit_name, c.city, c.country,
               r.fp1_date, r.fp1_time, r.fp2_date, r.fp2_time,
               r.fp3_date, r.fp3_time, r.qualifying_date, r.qualifying_time,
               r.sprint_date, r.sprint_time
        FROM race r 
        JOIN circuit c ON r.circuitid = c.circuitid
        WHERE r.raceid = :race_id
    """
    )

    cursor = g.conn.execute(query, {"race_id": race_id})
    race_data = cursor.fetchone()
    cursor.close()

    if race_data is not None:
        return render_template("race_detail.html", race=race_data)
    return render_template("not_found.html"), 404


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
