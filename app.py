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


global query, count, execution_time, pages, query_pages


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
    return render_template('success.html', q=query, page=current_page,
                           total_pages=len(pages), current_page=page_number, count=count,
                           execution_time=execution_time)


@app.route('/navigate')
def navigate():
    page_number = int(request.args.get('page', 1) or 1)
    _index = page_number - 1
    if 0 <= _index < len(query_pages):
        current_page = query_pages[_index]
    else:
        current_page = []
    return render_template('history.html', page=current_page,
                           current_page=page_number, total_pages=len(query_pages))


@app.route('/history')
def history():
    """
        Renders the history.html template for the history page.
    """
    global query_pages
    dbhandler = DBHandler()
    query_pages = dbhandler.get_queries()
    return redirect(url_for('navigate'))


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    """
        Processes the user's query and redirects to the search results page.
    """
    global query, count, execution_time, pages
    if request.method == 'POST':
        query = request.form.get('q')
    else:
        query = request.args.get('q')
    dbhandler = DBHandler()
    count, execution_time, pages = dbhandler.get(query)
    return redirect(url_for('index'))


if __name__ == '__main__':
    try:
        FlaskUI(app=app, server="flask").run()
    except KeyboardInterrupt:
        # This block will be executed when the FlaskUI window is closed abruptly.
        pass
    finally:
        driver_service.quit()
