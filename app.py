from flask import Flask, render_template, request
from src.helpers import process
import time
from flaskwebgui import FlaskUI

app = Flask(__name__)


@app.route('/')
def index():
    """
    Renders the index.html template for the home page.
    """
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    """
    Processes the user's query and returns the result.

    The function retrieves the user's query from the form submitted in the index.html page.
    It measures the execution time of the process() function by recording the start time before processing
    and the end time after processing. Then it renders the success.html template, passing the query,
    result, and execution time as parameters.
    """
    query = request.form.get('q')
    start_time = time.time()
    result = process(query)
    end_time = time.time()
    execution_time = round(end_time - start_time, 2)
    return render_template('success.html', q=query, result=result, execution_time=execution_time)


if __name__ == '__main__':
    """
        Run the Flask application with a graphical user interface.

        The FlaskUI class is used to run a Flask application with a graphical user interface (GUI).
        By calling the run() method on a FlaskUI object, the Flask application specified by app will be executed 
        with a GUI interface using the Flask development server.
    """
    FlaskUI(app=app, server="flask").run()
