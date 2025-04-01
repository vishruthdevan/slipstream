from flask import g, render_template
from sqlalchemy import text

from routes import drivers_bp


@drivers_bp.route("/<int:driver_id>/")
def driver_detail(driver_id):
    """Retrieve and display details for a specific driver."""
    query = text(
        "SELECT driverid, firstname, lastname, nationality, number FROM driver WHERE driverid = :driver_id"
    )
    cursor = g.conn.execute(query, {"driver_id": driver_id})
    driver_data = cursor.fetchone()
    cursor.close()

    if driver_data:
        return render_template("driver_detail.html", driver=driver_data)
    return render_template("not_found.html"), 404


@drivers_bp.route("/")
def drivers():
    """Retrieve and display drivers from the database along with podiums."""
    query = text(
        """
        SELECT d.driverid, firstname, lastname, nationality, 
               COALESCE(SUM(CASE WHEN rr.position <= 3 THEN 1 ELSE 0 END), 0) AS podiums
        FROM driver d
        LEFT JOIN raceresults rr ON rr.driverid = d.driverid
        GROUP BY d.driverid
        ORDER BY podiums DESC
    """
    )
    cursor = g.conn.execute(query)

    drivers_data = []
    for row in cursor:
        drivers_data.append(
            {
                "id": row[0],
                "name": f"{row[1]} {row[2]}",
                "nationality": row[3],
                "podiums": row[4],
            }
        )
    cursor.close()

    return render_template("drivers.html", drivers=drivers_data)
