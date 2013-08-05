#------------------------------------------------------------------------------#
# Imports
#------------------------------------------------------------------------------#

from flask import (Flask, jsonify, render_template, request)
import logging
from logging import Formatter, FileHandler
from helpers import bing_query, Elections

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
    """
    Asks user for address so we can give relevant voting information to them,
    and displays a list of elections for the user to choose from.
    """
    e = Elections()

    elections = e.get_elections()
    context = {'elections': elections}

    return render_template("index.html", **context)

@app.route("/elections", methods = ["POST"])
def elections():
    """
    Uses the election id and address provided to show user a list of contests
    consisting of candidates and information about them.
    """
    e = Elections()

    election_id = request.values['elections']
    address = request.values['street_address']
    zipcode = request.values['zipcode']
    s = address + ' ' + zipcode
    contests = e.get_voter_info(election_id, s)
    context = {'elections': contests, 'election_id': election_id, 'address': s}

    return render_template("elections.html", **context)

@app.route("/api/candidates")
def api_candidates():
    """
    Returns candidates for the office by `office_name`

    Example: http://localhost:4567/api/candidates?address=NJ+07302&election_id=4000&office_name=U.S.+Senate
    """
    e = Elections()

    election_id = request.args.get('election_id')
    address = request.args.get('address')
    office_name = request.args.get('office_name')
    contests = e.get_voter_info(election_id, address)

    candidates = {'candidates': contests}

    for contest in contests:
        if contest.get('office', 'fail') == office_name:
            candidates['candidates'] = contest.get('candidates')
            break

    return jsonify(**candidates)

@app.route("/api/elections")
def api_elections():
    """
    Returns elections
    """
    e = Elections()
    return jsonify(**{'elections': e.get_elections()})

@app.route("/api/offices")
def api_offices():
    """
    Returns offices by election and address

    Example: http://localhost:4567/api/offices?address=NJ+07302&election_id=4000
    """
    e = Elections()

    election_id = request.args.get('election_id')
    address = request.args.get('address')
    contests = e.get_voter_info(election_id, address)

    offices = {'offices': []}

    for contest in contests:
        office = contest.get('office')
        if office:
            offices['offices'].append(office)

    return jsonify(**offices)

@app.route("/dashboard")
def dashboard():
    issues = request.args.get('issues', '')

    return render_template("dashboard.html")

@app.route("/candidate")
def candidate():
    print request.values
    x = request.values
    candidate_name = x['name']
    issues = request.values['issues']
    news = bing_query(candidate_name, issues)
    context = {'news': news}
    return jsonify(**context)

@app.route("/choose")
def choose():
    return render_template("choose.html")

@app.route("/compare")
def compare():
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

