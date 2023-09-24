#!/usr/bin/python3
# Import necessary modules
from flask import Flask, render_template
from models import storage
from models.state import State
from flask import g

# Create a Flask web application
app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    # Get a list of all State objects sorted by name
    states = sorted(storage.all(State).values(), key=lambda state: state.name)

    # Render the HTML template with the list of states
    return render_template('states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    # A teardown function to close the SQLAlchemy session
    storage.close()


if __name__ == '__main__':
    # Run the Flask app on 0.0.0.0:5000
    app.run(host='0.0.0.0', port=5000)
