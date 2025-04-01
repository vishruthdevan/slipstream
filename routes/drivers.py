from flask import g, render_template
from sqlalchemy import text

from routes import drivers_bp


@drivers_bp.route("/<int:driver_id>/")
def driver_detail(driver_id):
    """Retrieve and display details for a specific driver."""

    # Driver Information
    query_driver = text(
        """
        SELECT driverid, firstname, lastname, nationality, number
        FROM driver WHERE driverid = :driver_id
    """
    )
    cursor_driver = g.conn.execute(query_driver, {"driver_id": driver_id})
    driver_data = cursor_driver.fetchone()
    cursor_driver.close()

    if not driver_data:
        return render_template("not_found.html"), 404

    # Driver Stats: Podiums, Wins, Total Points
    query_race_results = text(
        """
        SELECT COUNT(*) AS podiums, SUM(points) AS total_points
        FROM raceresults rr
        JOIN race r ON rr.raceid = r.raceid
        WHERE rr.driverid = :driver_id
    """
    )
    cursor_race_results = g.conn.execute(query_race_results, {"driver_id": driver_id})
    race_results = cursor_race_results.fetchone()
    cursor_race_results.close()

    query_wins = text(
        """
        SELECT COUNT(*) AS wins
        FROM raceresults rr
        WHERE rr.driverid = :driver_id AND rr.position = 1
    """
    )
    cursor_wins = g.conn.execute(query_wins, {"driver_id": driver_id})
    wins = cursor_wins.fetchone()
    cursor_wins.close()

    # Race Results with Performance
    query_performance = text(
        """
        SELECT r.name AS race_name, r.year, rr.position, rr.points
        FROM raceresults rr
        JOIN race r ON rr.raceid = r.raceid
        WHERE rr.driverid = :driver_id
        ORDER BY r.year ASC
    """
    )
    cursor_performance = g.conn.execute(query_performance, {"driver_id": driver_id})
    race_results_data = cursor_performance.fetchall()
    cursor_performance.close()

    # Laps Information (Total laps driven)
    query_laps = text(
        """
        SELECT SUM(lapid) AS total_laps
        FROM lap l
        JOIN race r ON l.raceid = r.raceid
        WHERE l.driverid = :driver_id
    """
    )
    cursor_laps = g.conn.execute(query_laps, {"driver_id": driver_id})
    laps_data = cursor_laps.fetchone()
    cursor_laps.close()

    # Best Performance (Highest finish position and race with max points)
    query_best_performance = text(
        """
        SELECT MIN(position) AS best_position, r.name AS best_race, rr.points AS best_points
        FROM raceresults rr
        JOIN race r ON rr.raceid = r.raceid
        WHERE rr.driverid = :driver_id
        GROUP BY r.name, rr.points
        ORDER BY rr.points DESC
        LIMIT 1
    """
    )
    cursor_best_performance = g.conn.execute(
        query_best_performance, {"driver_id": driver_id}
    )
    best_performance = cursor_best_performance.fetchone()
    cursor_best_performance.close()

    # Position Distribution for D3.js visualization
    query_position_distribution = text(
        """
        SELECT position, COUNT(*) AS position_count
        FROM raceresults rr
        WHERE rr.driverid = :driver_id
        GROUP BY position
        ORDER BY position
    """
    )
    cursor_position_distribution = g.conn.execute(
        query_position_distribution, {"driver_id": driver_id}
    )
    position_distribution = cursor_position_distribution.fetchall()
    cursor_position_distribution.close()

    # Convert Row objects into a list of dictionaries
    position_distribution_list = [
        {"position": row[0], "position_count": row[1]} for row in position_distribution
    ]

    return render_template(
        "driver_detail.html",
        driver=driver_data,
        race_results=race_results,
        wins=wins,
        race_results_data=race_results_data,
        laps_data=laps_data,
        best_performance=best_performance,
        position_distribution=position_distribution_list,
    )


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
        LIMIT 100;
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
