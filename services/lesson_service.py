# services/lesson_service.py

from db import dbConnection

def get_lessons_with_topics():
    conn = dbConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lessons")
    lessons = cursor.fetchall()
    
    for lesson in lessons:
        cursor.execute("SELECT * FROM topics WHERE lesson_id = %s", (lesson['id'],))
        lesson['topics'] = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return lessons
