from flask import g, render_template, request
from sqlalchemy import text

from routes import standings_bp


@standings_bp.route("/")
def standings():
    """Retrieve and display driver standings for a given year."""
    year = request.args.get("year", None)  # Get the year from query parameters

    # If no year is provided, get the latest year
    if year is None:
        latest_year_query = text("SELECT MAX(year) FROM seasonstandings")
        latest_year = g.conn.execute(latest_year_query).scalar()
        year = latest_year

    # Query to fetch driver standings for the given year
    standings_query = text(
        """
        SELECT d.driverid, d.firstname, d.lastname, ss.points, 
               COALESCE(wins.wins, 0) AS wins
        FROM seasonstandings ss
        JOIN driver d ON ss.driverid = d.driverid
        LEFT JOIN (
            SELECT rr.driverid, COUNT(*) AS wins
            FROM raceresults rr
            JOIN race r ON rr.raceid = r.raceid
            WHERE rr.position = 1 AND r.year = :year
            GROUP BY rr.driverid
        ) wins ON ss.driverid = wins.driverid
        WHERE ss.year = :year
        ORDER BY ss.points DESC
        """
    )

    cursor = g.conn.execute(standings_query, {"year": year})
    standings_data = []
    for row in cursor:
        standings_data.append(
            {
                "driver_id": row[0],
                "name": f"{row[1]} {row[2]}",
                "points": row[3],
                "wins": row[4],
            }
        )
    cursor.close()

    return render_template("standings.html", standings=standings_data, selected_year=year)
