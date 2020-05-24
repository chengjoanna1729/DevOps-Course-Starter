from flask import Flask, render_template, request, redirect, url_for
import session_items as session

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/')
def index():
    items = sorted(session.get_items(), key=lambda i: i['status'], reverse=True)
    return render_template('index.html', items=items)
    
@app.route('/', methods=['POST'])
def add_item():
    title = request.form['item_title']
    session.add_item(title)
    return redirect(url_for('index'))

@app.route('/items/<id>', methods=['POST'])
def mark_item_as_complete(id):
    item = session.get_item(id)
    item['status'] = 'Completed'
    session.save_item(item)
    return redirect(url_for('index'))

@app.route('/items/delete/<id>', methods=['POST'])
def delete_item(id):
    item = session.get_item(id)
    session.remove_item(item)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
