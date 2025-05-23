from flask import Blueprint, render_template, request
from db import dbConnection

lesson_bp = Blueprint('lesson', __name__, url_prefix='/lessons')

@lesson_bp.route('/<int:lesson_id>')
def view_lesson(lesson_id):
    conn = dbConnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM lessons WHERE id=%s", (lesson_id,))
    lesson = cursor.fetchone()

    cursor.execute("SELECT * FROM topics WHERE lesson_id=%s", (lesson_id,))
    topics = cursor.fetchall()

    selected_topic_id = request.args.get('topic_id')
    if not selected_topic_id and topics:
        selected_topic_id = topics[0]['id']

    contents = []
    if selected_topic_id:
        cursor.execute("SELECT * FROM contents WHERE topic_id=%s", (selected_topic_id,))
        contents = cursor.fetchall()

    conn.close()

    return render_template("lesson_view.html", lesson=lesson, topics=topics,
                           contents=contents, selected_topic_id=int(selected_topic_id))
