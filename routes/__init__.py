from flask import Blueprint

# Create blueprints for modular routing
main_bp = Blueprint("main", __name__)
circuits_bp = Blueprint("circuits", __name__)
races_bp = Blueprint("races", __name__)
constructors_bp = Blueprint("constructors", __name__)
drivers_bp = Blueprint("drivers", __name__)
standings_bp = Blueprint("standings", __name__)
constructor_standings_bp = Blueprint("constructor_standings", __name__)
qualifying_results_bp = Blueprint("qualifying_results", __name__)
race_results_bp = Blueprint("race_results", __name__)
sprint_results_bp = Blueprint("sprint_results", __name__)
laps_bp = Blueprint("laps", __name__)


# Import routes to register them
from routes import (
    circuits,
    constructor_standings,
    constructors,
    drivers,
    laps,
    main,
    qualifying_results,
    race_results,
    races,
    sprint_results,
    standings,
)
