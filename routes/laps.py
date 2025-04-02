from flask import Blueprint, g, render_template, request
from sqlalchemy.sql import text

from routes import laps_bp


@laps_bp.route("/")
def lap_information():
    """Retrieve and display lap data filtered by race (mandatory), and optionally by driver and constructor."""
    race_id = request.args.get("race_id")
    driver_id = request.args.get("driver_id")
    constructor_id = request.args.get("constructor_id")

    # Fetch available races, drivers, and constructors
    races_query = text("SELECT raceid, name FROM race ORDER BY date DESC")
    drivers_query = text(
        "SELECT driverid, firstname || ' ' || lastname FROM driver ORDER BY lastname"
    )
    constructors_query = text(
        "SELECT constructorid, name FROM constructor ORDER BY name"
    )

    races = g.conn.execute(races_query).fetchall()
    drivers = g.conn.execute(drivers_query).fetchall()
    constructors = g.conn.execute(constructors_query).fetchall()

    lap_data = []
    if race_id:
        query = """
            SELECT l.lapnumber, l.position, l.laptime, 
                   d.firstname || ' ' || d.lastname AS driver_name, 
                   c.name AS constructor_name,
                   r.name AS race_name,
                   r.date,
                   p.duration
            FROM lap l
            LEFT JOIN pitstop p ON l.lapid = p.lapid
            JOIN race r ON l.raceid = r.raceid AND l.raceid = :race_id
            JOIN driver d ON l.driverid = d.driverid
            JOIN constructor c ON l.constructorid = c.constructorid
        """

        params = {"race_id": race_id}

        if driver_id:
            query += " AND l.driverid = :driver_id"
            params["driver_id"] = driver_id

        if constructor_id:
            query += " AND l.constructorid = :constructor_id"
            params["constructor_id"] = constructor_id

        query += " ORDER BY l.lapnumber ASC"

        cursor = g.conn.execute(text(query), params)
        lap_data = cursor.fetchall()
        cursor.close()

        lap_data = [
            {
                "lap_number": row[0],
                "position": row[1],
                "lap_time": str(row[2]),
                "driver_name": row[3],
                "constructor_name": row[4],
                "race_name": row[5],
                "date": row[6],
                "pit_stop_duration": str(row[7]) if row[7] else None,
            }
            for row in lap_data
        ]

    return render_template(
        "laps.html",
        lap_data=lap_data,
        races=races,
        drivers=drivers,
        constructors=constructors,
        selected_race=race_id,
        selected_driver=driver_id,
        selected_constructor=constructor_id,
    )
