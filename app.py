from flask import Flask
from services.lesson_service import get_lessons_with_topics
from controllers.home_controller import home_bp
from controllers.lesson_controller import lesson_bp
# from controllers.post_controller import post_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(lesson_bp)
# app.register_blueprint(post_bp)

@app.context_processor
def inject_sidebar_data():
    lessons = get_lessons_with_topics()
    
    return dict(lessons=lessons)

if __name__ == '__main__':
    app.run(debug=True)