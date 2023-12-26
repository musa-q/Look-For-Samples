from flask import Flask
from datetime import timedelta
from .views import views_bp

app = Flask(__name__)
app.register_blueprint(views_bp)
app.secret_key = 'SECRET_KEY'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

if __name__ == '__main__':
    app.run()
