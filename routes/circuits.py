from flask import g, render_template
from sqlalchemy import text

from routes import circuits_bp


@circuits_bp.route("/<int:circuit_id>/")
def circuit_detail(circuit_id):
    """Retrieve and display details for a specific circuit, including top constructors, drivers, and races."""

    # Fetch circuit details
    query_circuit = text(
        """
        SELECT name, city, country, latitude, longitude
        FROM circuit
        WHERE circuitid = :circuit_id;
    """
    )
    cursor = g.conn.execute(query_circuit, {"circuit_id": circuit_id})
    circuit_data = cursor.fetchone()
    cursor.close()

    if not circuit_data:
        return render_template("not_found.html"), 404

    # Fetch top 3 constructors by wins
    query_top_constructors = text(
        """
        SELECT c.constructorid, c.name, COUNT(res.raceid) AS wins
        FROM raceresults res
        JOIN race r ON res.raceid = r.raceid
        JOIN constructor c ON res.constructorid = c.constructorid
        WHERE r.circuitid = :circuit_id AND res.position = 1
        GROUP BY c.constructorid, c.name
        ORDER BY wins DESC
        LIMIT 3;
    """
    )
    top_constructors = g.conn.execute(
        query_top_constructors, {"circuit_id": circuit_id}
    ).fetchall()

    # Fetch top 3 drivers by wins
    query_top_drivers = text(
        """
        SELECT d.driverid, CONCAT(d.firstname, ' ', d.lastname) AS name, COUNT(res.raceid) AS wins
        FROM raceresults res
        JOIN race r ON res.raceid = r.raceid
        JOIN driver d ON res.driverid = d.driverid
        WHERE r.circuitid = :circuit_id AND res.position = 1
        GROUP BY d.driverid, d.firstname, d.lastname
        ORDER BY wins DESC
        LIMIT 3;
    """
    )
    top_drivers = g.conn.execute(
        query_top_drivers, {"circuit_id": circuit_id}
    ).fetchall()

    # Fetch all races at this circuit
    query_races = text(
        """
        SELECT raceid, year, name
        FROM race
        WHERE circuitid = :circuit_id
        ORDER BY year DESC;
    """
    )
    races = g.conn.execute(query_races, {"circuit_id": circuit_id}).fetchall()

    return render_template(
        "circuit_detail.html",
        circuit=circuit_data,
        top_constructors=top_constructors,
        top_drivers=top_drivers,
        races=races,
    )


@circuits_bp.route("/")
def circuits():
    """Retrieve and display circuits from the database."""
    query = text(
        "SELECT circuitid, name, city, country, latitude, longitude FROM circuit"
    )
    cursor = g.conn.execute(query)

    circuits_data = []
    for row in cursor:
        circuits_data.append(
            {
                "id": row[0],
                "name": row[1],
                "city": row[2],
                "country": row[3],
                "latitude": row[4],
                "longitude": row[5],
            }
        )
    cursor.close()

    return render_template("circuits.html", circuits=circuits_data)
