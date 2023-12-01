from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    #  Define routes directly here
    @app.route('/')
    def index():
        return "Welcome to Litigate!"
    @app.route('/home')
    def home():
        return render_template('index.html')

    return app

  
