from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://user:password@localhost/restaurant_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')

    # Serve static files from client directory
    app.static_folder = '../client'

    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    # Register blueprints
    from server.routes.auth_routes import auth_bp
    from server.routes.reservation_routes import reservation_bp
    from server.routes.menu_routes import menu_bp
    from server.routes.order_routes import order_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(reservation_bp, url_prefix='/reservations')
    app.register_blueprint(menu_bp, url_prefix='/menu')
    app.register_blueprint(order_bp, url_prefix='/orders')

    # Add route to serve index.html
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    # Serve other static files
    @app.route('/<path:filename>')
    def static_files(filename):
        return app.send_static_file(filename)

    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
