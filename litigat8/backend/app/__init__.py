from flask import *
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from database.db import db
from database.db import *
import requests
import openai
from openai import OpenAI
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/litigat8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your secret key'
    responses = []
    interactions = []
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
   
    def get_ai_response(prompt):
        print(prompt)
        messages = []
        client = OpenAI(
            api_key="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",
        )
        messages.append( {"role": "system", "content": "As an AI legal assistant specializing in household and tenant law, your task is to provide users with comprehensive information on the rights and responsibilities of tenants and landlords. You should be equipped to discuss lease agreements, rent control, eviction processes, and other relevant legal matters. Be prepared to reference case laws and legal resources when necessary to support your advice. It's important that your responses are clear, accurate, and reflect the most current legal standards and practices. Your goal is to assist users in understanding their legal position and options in a variety of scenarios related to tenancy and property law."})
        messages.append( {"role": "user", "content": prompt })

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
           
            messages=messages
            )
      
        print(messages)
        if response:
            messages.append(response.choices[0].message.content)
            return response.choices[0].message.content
        else:
            return "I'm sorry, I couldn't process that request."
    
    
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('You need to be logged in to view this page.')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    
    @app.route('/main',methods=['GET'])
    def main():
        return render_template('welcome_page.html')

    @app.route('/',methods=['GET'])
    def index():
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                return render_template('index.html', user=user)
            else:
       
                return redirect(url_for('main'))  
        else:
            # Handle case where user is not logged in

            return redirect(url_for('main'))

    @app.route('/chat',methods=['GET'])
    @login_required
    def home():
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                return render_template('index.html', user=user)
            else:
                flash('You need to be logged in to view this page.')
                return redirect(url_for('login'))  
        else:
            # Handle case where user is not logged in
            flash('You need to be logged in to view this page.')
            return redirect(url_for('login'))
        
        
    
    @app.route('/submit', methods=['GET', 'POST'])
    def submit():
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        if request.method == 'POST':
            user_input = request.form['user_input']
            
            # Simulate an AI response (replace with your actual AI logic)
            ai_response =  get_ai_response(f"Tenant Law Question: {user_input}\nAnswer:")
            ai_response = "s an AI legal assistant specializing in household and tenant law, your task is to provide users with comprehensive information on the rights and responsibilities of tenants and landlords. You should be equipped to discuss lease agreements, rent control, eviction processes, and other relevant legal matters. Be prepared to reference case laws and legal resources when necessary to support your advice. It's important that your responses are clear, accurate, and reflect the most current legal standards and practices. Your goal is to assist users in understanding their legal position"
            # Append user input and AI response to the interactions list
    
            interactions.append({'type': 'user', 'text': user_input})
            interactions.append({'type': 'ai', 'text': ai_response})
            

        return render_template('index.html', interactions=interactions,user=user)

        # # If it's a GET request, just render the template with existing responses
        # return render_template('index.html', responses=responses)
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password.')
                pass
        return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        interactions.clear()
        session.pop('user_id', None)
        return redirect(url_for('main'))
    return app

    # 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