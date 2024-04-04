from flask import *
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .extensions import db
import requests
import openai
from openai import OpenAI
import os
from .database.models import *
from datetime import datetime
from .blueprints.auth import auth
from .blueprints.chat import chat
def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:8080/litigat8'

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/litigat8'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@viaduct.proxy.rlwy.net:58016/litigat8'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your secret key'

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(chat, url_prefix='/chat')
    db.init_app(app)
    with app.app_context():
        db.create_all()
   
   
    
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('You need to be logged in to view this page.')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    


    @app.route('/',methods=['GET'])
    def index():
        user_id = session.get('user_id')
        if user_id:
            user = session.get('user_id')
            if user:
                return redirect(url_for('main_chat')) 
            else:
       
                return render_template('welcome_page.html') 
        else:
            return render_template('welcome_page.html')

    @app.route('/chat',methods=['GET'])
    @login_required
    def main_chat():
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                return render_template('index.html', user=user)
            else:
                flash('You need to be logged in to view this page.')
                return redirect(url_for('index'))  
        else:
            # Handle case where user is not logged in
            flash('You need to be logged in to view this page.')
            return redirect(url_for('index'))
        
    return app
        
   
# if __name__ == '__main__':

#     app.run(debug=True)
    

