from flask import *
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from database.db import db
from database.db import *
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
    # Define routes directly here
   
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
        if request.method == 'POST':
            user_input = request.form['user_input']
            
            # Simulate an AI response (replace with your actual AI logic)
            ai_response = f"Litigat8 responded to: {user_input}"

            # Append user input and AI response to the interactions list
            interactions.append({'type': 'user', 'text': user_input})
            interactions.append({'type': 'ai', 'text': ai_response})

        return render_template('index.html', interactions=interactions)

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