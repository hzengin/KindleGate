from flask import Flask, render_template, request, redirect
from Utilities import *
from Authentication import *
app = Flask(__name__)

@app.route('/')
@requires_auth
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST', 'GET'])  # post for searching get for listing all
@requires_auth
def search():
    if request.method == 'POST':  # this is a search request
        keyword = request.form['keyword']
    else:
        keyword = ""  # every string contains empty string
    result = [{'link': create_link(epub), 'name': epub} for epub in get_epubs(epub_directory_path, keyword=keyword)]
    return render_template('result.html', keyword=keyword, results=result)

@app.route('/ebook/<name>', methods=['GET'])  # convert and send me book
@requires_auth
def get_ebook(name):
    real_name = base64_to_str(name)
    return redirect(convert_ebook(real_name))

if __name__ == '__main__':
    app.run()
