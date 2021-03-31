from flask import Flask, render_template, request, redirect, url_for
from mongodb import MongoDB
from oauth import OAuthClient
from flask_login import LoginManager, login_required, login_user, current_user
from view_model import ViewModel

def create_app():
    app = Flask(__name__)
    db = MongoDB()

    login_manager = LoginManager()
    login_manager.init_app(app)
    oauth = OAuthClient()

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(oauth.redirect_to_github())

    @login_manager.user_loader
    def load_user():
        return None

    @app.route('/login/callback')
    def login():
        oauth.get_access_token(request.url)
        # return redirect(url_for('index'))

    @app.route('/')
    @login_required
    def index():
        items = db.get_items()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)
        
    @app.route('/', methods=['POST'])
    @login_required
    def add_item():
        title = request.form['item_title']
        db.add_item(title)
        return redirect(url_for('index'))

    @app.route('/items/<id>', methods=['POST'])
    @login_required
    def mark_item_as_complete(id):
        db.mark_as_complete(id)
        return redirect(url_for('index'))

    @app.route('/items/delete/<id>', methods=['POST'])
    @login_required
    def delete_item(id):
        db.remove_item(id)
        return redirect(url_for('index'))

    return app
