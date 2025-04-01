from flask import g, render_template
from sqlalchemy import text

from routes import circuits_bp


@circuits_bp.route("/<int:circuit_id>/")
def circuit_detail(circuit_id):
    """Retrieve and display details for a specific circuit."""
    query = text(
        """
        SELECT name, city, country, latitude, longitude
        FROM circuit
        WHERE circuitid = :circuit_id;
    """
    )

    cursor = g.conn.execute(query, {"circuit_id": circuit_id})

    circuit_data = cursor.fetchone()
    cursor.close()

    if circuit_data:
        return render_template("circuit_detail.html", circuit=circuit_data)
    return render_template("not_found.html"), 404


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
