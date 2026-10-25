from app import app
from extensions import db
from models import Course

def seed_java_course():
    with app.app_context():
        # Check if course already exists to prevent duplicate entries
        existing_course = Course.query.filter_by(course_code='CS102').first()
        
        if existing_course:
            print("Course CS102 (JAVA) already exists in the database.")
            return

        # Add Java Course manually
        java_course = Course(
            course_code='CS102',
            course_name='JAVA',
            description='Core Java Programming Course'
        )
        
        db.session.add(java_course)
        db.session.commit()
        print(f"Successfully added manual course: {java_course.course_name} (ID: {java_course.id})")

if __name__ == '__main__':
    seed_java_course()