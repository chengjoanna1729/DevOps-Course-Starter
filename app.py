from flask import Flask, render_template, request, redirect, url_for
import trello

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/')
def index():
    items = sorted(trello.get_items(), key=lambda i: i.status, reverse=True)
    return render_template('index.html', items=items)
    
@app.route('/', methods=['POST'])
def add_item():
    title = request.form['item_title']
    trello.add_item(title)
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
