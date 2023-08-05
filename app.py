from flask import Flask, render_template, request
from src.process import process
from flaskwebgui import FlaskUI
from src.driver import driver_service

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
    Processes the user's query and returns the result to the submit page.
    """
    query = request.form.get('q')
    count, execution_time, result = process(query)
    return render_template('success.html', q=query, result=result, count=count, execution_time=execution_time)


if __name__ == '__main__':
    driver_service.start()
    FlaskUI(app=app, server="flask").run()
    driver_service.stop()
