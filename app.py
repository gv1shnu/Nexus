from flask import Flask, render_template, request, redirect, url_for
from src.db_handler import DBHandler
from flaskwebgui import FlaskUI
from src.driver import driver_service

app = Flask(__name__)


@app.route('/')
def home():
    """
        Renders the index.html template for the home page.
    """
    return render_template('index.html')


global query, count, execution_time, pages


@app.route('/index')
def index():
    """
        Renders the search results page template for specified page.
    """
    page_number = int(request.args.get('page', 1))
    _index = page_number - 1
    if 0 <= _index < len(pages):
        current_page = pages[_index]
    else:
        current_page = []
    total_pages = len(pages)
    return render_template('success.html', q=query, page=current_page,
                           total_pages=total_pages, current_page=page_number, count=count,
                           execution_time=execution_time)


@app.route('/submit', methods=['POST'])
def submit():
    """
        Processes the user's query and redirects to the search results page.
    """
    global query, count, execution_time, pages
    query = request.form.get('q')
    dbhandler = DBHandler()
    count, execution_time, pages = dbhandler.get(query)
    return redirect(url_for('index'))


if __name__ == '__main__':
    driver_service.start()
    FlaskUI(app=app, server="flask").run()
    driver_service.stop()
