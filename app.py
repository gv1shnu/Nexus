import webbrowser
from flask import Flask, render_template, request, redirect, url_for, jsonify
from src.db_handler import DBHandler
from flaskwebgui import FlaskUI
import logging

app = Flask(__name__)
app.debug = False
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
log.disabled = True
app.logger.disabled = True


@app.route('/')
def home():
    return render_template('index.html')


global query, count, execution_time, pages, query_pages


def get_current_page(page_number: int, data_list: list) -> list:
    _index = page_number - 1
    if 0 <= _index < len(data_list):
        current_page = data_list[_index]
    else:
        current_page = []
    return current_page


@app.route('/index')
def index():
    page_number = int(request.args.get('page', 1))
    current_page = get_current_page(page_number, pages)
    return render_template('success.html', q=query, page=current_page,
                           total_pages=len(pages), current_page=page_number,
                           count=count, execution_time=execution_time)


@app.route('/navigate')
def navigate():
    page_number = int(request.args.get('page', 1) or 1)
    current_page = get_current_page(page_number, query_pages)
    return render_template('history.html', page=current_page,
                           current_page=page_number, total_pages=len(query_pages))


@app.route('/history')
def history():
    global query_pages
    dbhandler = DBHandler()
    query_pages = dbhandler.get_queries()
    return redirect(url_for('navigate'))


@app.route('/submit', methods=['GET'])
def submit():
    global query, count, execution_time, pages
    query = request.args.get('q')
    dbhandler = DBHandler()
    count, execution_time, pages = dbhandler.get(query)
    return redirect(url_for('index'))


@app.route('/clear', methods=['POST'])
def clear_browsing_data():
    dbhandler = DBHandler()
    if dbhandler.clear():
        return jsonify({'message': 'Browsing data cleared successfully'}), 200
    else:
        return jsonify({'message': 'An error occurred'}), 500


if __name__ == '__main__':
    port = 8080
    # To run like a desktop app

    ui = FlaskUI(app=app, server="flask", port=port).run()

    # To run on browser

    # webbrowser.open(f'http://127.0.0.1:{port}/')
    # app.run(port=port)


