#------------------------------------------------------------------------------#
# Imports
#------------------------------------------------------------------------------#

from flask import (Flask, render_template)
import logging
from logging import Formatter, FileHandler

#------------------------------------------------------------------------------#
# App Config
#------------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

#------------------------------------------------------------------------------#
# Controllers
#------------------------------------------------------------------------------#

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/elections")
def login():
    return render_template("elections.html")

@app.route("/dashboard")
def register():
    return render_template("dashboard.html")

@app.route("/candidate/<cadidate_name>")
def register():
    return render_template("candidate.html")

@app.route("/choose")
def register():
    return render_template("choose.html")

@app.route("/compare")
def register():
    return render_template("compare.html")

# Error Handlers

@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('500.html'), 500

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

#------------------------------------------------------------------------------#
# Launch
#------------------------------------------------------------------------------#

# or specify port
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

