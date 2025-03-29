import os

from dotenv import load_dotenv
from flask import Flask, g, redirect, render_template, request

from config.database import engine
from routes import (
    circuits_bp,
    constructor_standings_bp,
    constructors_bp,
    drivers_bp,
    main_bp,
    qualifying_results_bp,
    race_results_bp,
    races_bp,
    sprint_results_bp,
    standings_bp,
)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.register_blueprint(main_bp)
app.register_blueprint(circuits_bp, url_prefix="/circuits")
app.register_blueprint(races_bp, url_prefix="/races")
app.register_blueprint(constructors_bp, url_prefix="/constructors")
app.register_blueprint(drivers_bp, url_prefix="/drivers")
app.register_blueprint(standings_bp, url_prefix="/standings")
app.register_blueprint(constructor_standings_bp, url_prefix="/constructor-standings")
app.register_blueprint(qualifying_results_bp, url_prefix="/qualifying-results")
app.register_blueprint(sprint_results_bp, url_prefix="/sprint-results")
app.register_blueprint(race_results_bp, url_prefix="/race-results")


@app.before_request
def before_request():
    """Establish database connection before each request."""
    try:
        g.conn = engine.connect()
    except:
        print("Error: Unable to connect to database")
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    """Close database connection after each request."""
    try:
        g.conn.close()
    except:
        pass


@app.route("/")
def index():
    """Render the home page."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8111)
