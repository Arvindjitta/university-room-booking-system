from flask import Flask, render_template, redirect, url_for
from config import Config
from routes.auth_routes import auth_bp
from routes.reservation_routes import reservation_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)
app.config.from_object(Config)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(reservation_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
