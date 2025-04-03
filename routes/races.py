from flask import g, render_template, request
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
    year = request.args.get("year", None)

    if year is None:
        latest_year_query = text("SELECT MAX(year) FROM race")
        latest_year = g.conn.execute(latest_year_query).scalar()
        year = latest_year

    query = text("SELECT raceid, name, year, date FROM race WHERE year = :year")
    cursor = g.conn.execute(query, {"year": year})

    races_data = []
    for row in cursor:
        races_data.append({"id": row[0], "name": row[1], "year": row[2], "date": row[3]})
    cursor.close()

    return render_template("races.html", races=races_data, selected_year=year)
