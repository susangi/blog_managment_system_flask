from flask import Flask
from services.lesson_service import get_lessons_with_topics
from controllers.home_controller import home_bp
from controllers.login_controller import admin_login_bp
from controllers.blog_controller import blog_bp
from controllers.blog_admin_controller import blog_admin_bp
from config import SECRET_KEY
import os

app = Flask(__name__)
app.secret_key = SECRET_KEY 
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'img')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

# Define the routes
# Register Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(admin_login_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(blog_admin_bp)

@app.context_processor
def inject_sidebar_data():
    lessons = get_lessons_with_topics()

    return dict(lessons=lessons)

if __name__ == '__main__':
    app.run(debug=True)