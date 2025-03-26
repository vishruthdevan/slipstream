from flask import Blueprint

# Create blueprints for modular routing
main_bp = Blueprint("main", __name__)
circuits_bp = Blueprint("circuits", __name__)
races_bp = Blueprint("races", __name__)
constructors_bp = Blueprint("constructors", __name__)
drivers_bp = Blueprint("drivers", __name__)
standings_bp = Blueprint("standings", __name__)

# Import routes to register them
from routes import circuits, constructors, drivers, main, races, standings
