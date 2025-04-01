from flask import g, render_template, request
from sqlalchemy import text

from routes import constructor_standings_bp


@constructor_standings_bp.route("/")
def constructor_standings():
    """Retrieve and display constructor standings for a given year."""
    year = request.args.get("year", None)  # Get the year from query parameters

    # If no year is provided, get the latest year
    if year is None:
        latest_year_query = text("SELECT MAX(year) FROM constructorstandings")
        latest_year = g.conn.execute(latest_year_query).scalar()
        year = latest_year

    # Query to fetch constructor standings for the given year
    standings_query = text(
        """
        SELECT cs.constructorid, c.name, cs.points, cs.rank, cs.year
        FROM constructorstandings cs
        JOIN constructor c ON cs.constructorid = c.constructorid
        WHERE cs.year = :year
        ORDER BY cs.points DESC
    """
    )

    standings_cursor = g.conn.execute(standings_query, {"year": year})

    standings_data = []
    for row in standings_cursor:
        standings_data.append(
            {
                "constructor_id": row[0],
                "name": row[1],
                "points": row[2],
                "rank": row[3],
                "year": row[4],
                "drivers": [],  # Placeholder for driver data
            }
        )

    standings_cursor.close()

    # Fetch drivers and points for each constructor
    driver_query = text(
        """
        SELECT d.firstname, d.lastname, r.constructorid, SUM(r.points) AS driver_points
        FROM raceresults r
        JOIN driver d ON r.driverid = d.driverid
        JOIN race ra ON r.raceid = ra.raceid
        WHERE ra.year = :year
        GROUP BY d.driverid, r.constructorid
        ORDER BY driver_points DESC
    """
    )

    driver_cursor = g.conn.execute(driver_query, {"year": year})
    driver_data = driver_cursor.fetchall()
    driver_cursor.close()

    # Map drivers to their constructors
    for driver in driver_data:
        for standing in standings_data:
            if standing["constructor_id"] == driver[2]:  # Match constructor ID
                standing["drivers"].append(
                    {"name": f"{driver[0]} {driver[1]}", "points": driver[3]}
                )

    return render_template(
        "constructor_standings.html", standings=standings_data, selected_year=year
    )
