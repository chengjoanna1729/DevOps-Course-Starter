from flask import Flask, render_template, request, redirect, url_for
from mongodb import MongoDB
from view_model import ViewModel

def create_app():
    app = Flask(__name__)
    db = MongoDB()

    @app.route('/')
    def index():
        items = db.get_items()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)
        
    @app.route('/', methods=['POST'])
    def add_item():
        title = request.form['item_title']
        db.add_item(title)
        return redirect(url_for('index'))

    @app.route('/items/<id>', methods=['POST'])
    def mark_item_as_complete(id):
        db.mark_as_complete(id)
        return redirect(url_for('index'))

    @app.route('/items/delete/<id>', methods=['POST'])
    def delete_item(id):
        db.remove_item(id)
        return redirect(url_for('index'))

    return app
