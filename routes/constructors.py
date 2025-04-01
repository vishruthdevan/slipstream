from flask import g, render_template
from sqlalchemy import text

from routes import constructors_bp


@constructors_bp.route("/<int:constructor_id>/")
def constructor_detail(constructor_id):
    """Retrieve and display details for a specific constructor, including statistics and associated drivers."""

    # Query for basic constructor info
    constructor_query = text(
        """
        SELECT constructorid, name, nationality 
        FROM constructor 
        WHERE constructorid = :constructor_id
        """
    )
    constructor = g.conn.execute(
        constructor_query, {"constructor_id": constructor_id}
    ).fetchone()

    if not constructor:
        return render_template("not_found.html"), 404

    # Query for total points and championships
    stats_query = text(
        """
        SELECT 
            COALESCE(SUM(cs.Points), 0) AS total_points,
            COUNT(DISTINCT CASE WHEN cs.Rank = 1 THEN cs.Year END) AS total_championships
        FROM ConstructorStandings cs
        WHERE cs.ConstructorID = :constructor_id
        """
    )
    stats = g.conn.execute(stats_query, {"constructor_id": constructor_id}).fetchone()

    total_points = stats[0] if stats else 0
    total_championships = stats[1] if stats else 0

    # Query for total podium finishes
    podium_query = text(
        """
        SELECT COUNT(*) 
        FROM RaceResults 
        WHERE ConstructorID = :constructor_id 
        AND Position BETWEEN 1 AND 3
        """
    )
    podiums = (
        g.conn.execute(podium_query, {"constructor_id": constructor_id}).scalar() or 0
    )

    # Query for all drivers associated with the constructor
    drivers_query = text(
        """
            SELECT d.driverid, d.firstname, d.lastname, d.nationality, 
                   COUNT(rr.position) AS podiums
            FROM driver d
            JOIN raceresults rr ON rr.driverid = d.driverid
            JOIN race r ON rr.raceid = r.raceid
            WHERE rr.constructorid = :constructor_id AND rr.position IN (1, 2, 3)
            GROUP BY d.driverid
        """
    )
    drivers = g.conn.execute(
        drivers_query, {"constructor_id": constructor_id}
    ).fetchall()

    # Prepare driver data
    drivers_list = [
        {"id": d[0], "name": f"{d[1]} {d[2]}", "nationality": d[3], "podiums": d[4]}
        for d in drivers
    ]

    return render_template(
        "constructor_detail.html",
        constructor=constructor,
        total_points=total_points,
        total_championships=total_championships,
        podiums=podiums,
        drivers=drivers_list,
    )


@constructors_bp.route("/")
def constructors():
    """Retrieve and display constructors with podium counts and championships."""
    query = text(
        """
        SELECT c.constructorid, c.name, c.nationality, 
               COALESCE(p.podiums, 0) AS total_podiums, 
               COALESCE(ch.championships, 0) AS championships
        FROM constructor c
        LEFT JOIN (
            SELECT constructorid, COUNT(*) AS podiums 
            FROM raceresults 
            WHERE position IN (1, 2, 3) 
            GROUP BY constructorid
        ) p ON c.constructorid = p.constructorid
        LEFT JOIN (
            SELECT constructorid, COUNT(*) AS championships 
            FROM constructorstandings 
            WHERE rank = 1 
            GROUP BY constructorid
        ) ch ON c.constructorid = ch.constructorid
        ORDER BY championships DESC, total_podiums DESC;
        """
    )

    cursor = g.conn.execute(query)
    constructors_data = []
    for row in cursor:
        constructors_data.append(
            {
                "id": row[0],
                "name": row[1],
                "nationality": row[2],
                "total_podiums": row[3],
                "championships": row[4],
            }
        )
    cursor.close()

    return render_template("constructors.html", constructors=constructors_data)
