from flask import Flask, render_template, request, redirect, url_for
import trello
from view_model import ViewModel

app = Flask(__name__)

@app.route('/')
def index():
    items = sorted(trello.get_items(), key=lambda i: i.status, reverse=True)
    item_view_model = ViewModel(items)
    return render_template('index.html', view_model=item_view_model)
    
@app.route('/', methods=['POST'])
def add_item():
    title = request.form['item_title']
    description = request.form['item_description']
    trello.add_item(title, description)
    return redirect(url_for('index'))

@app.route('/items/<id>', methods=['POST'])
def mark_item_as_complete(id):
    trello.mark_as_complete(id)
    return redirect(url_for('index'))

@app.route('/items/delete/<id>', methods=['POST'])
def delete_item(id):
    trello.remove_item(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
