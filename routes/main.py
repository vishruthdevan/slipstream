from flask import render_template

from routes import main_bp


@main_bp.route("/")
def index():
    """Render the home page."""
    return render_template("index.html")
