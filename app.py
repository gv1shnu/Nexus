from flask import Flask, render_template, request
from src.helpers import process
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
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
    Processes the user's query and returns the result to the submit page.
    """
    query = request.form.get('q')
    start_time = time.time()
    global driver_service
    result = process(query, driver_service)
    end_time = time.time()
    execution_time = round(end_time - start_time, 2)
    return render_template('success.html', q=query, result=result, execution_time=execution_time)


if __name__ == '__main__':
    driver_service = webdriver.chrome.service.Service(ChromeDriverManager().install())
    FlaskUI(app=app, server="flask").run()
