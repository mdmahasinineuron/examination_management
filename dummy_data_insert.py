from datetime import date, timedelta
from app import app
from extensions import db
from models import Course, Examination


def seed_examinations():
  with app.app_context():
    # 1. Foreign Key requirement: Pehle check karo koi Course exist karta hai ya nahi
    course = Course.query.first()

    if not course:
      # Agar koi course nahi hai, toh temporary course bana dete hain
      course = Course(
          course_code='CS102',
          course_name='JAVA',
          description='Sample Course for Exam Data',
      )
      db.session.add(course)
      db.session.commit()
      print(f'Created sample course with ID: {course.id}')

    today = date.today()

    # 2. Sample Examinations Data Definition
    dummy_exams = [
        # Active Exam (Active Exams count test karne ke liye)
        Examination(
            course_id=course.id,
            name='Mid-Term Practical 2026',
            exam_type='Practical',  #
            start_date=today - timedelta(days=2),  # Start: 2 din pehle
            end_date=today + timedelta(days=5),  # End: 5 din baad
            slot_creation_start=today - timedelta(days=10),
            slot_creation_end=today - timedelta(days=6),
            slot_booking_start=today - timedelta(days=5),
            slot_booking_end=today + timedelta(days=2),
            status='Booking Open',  #
        ),
        # Upcoming Exam (Future)
        Examination(
            course_id=course.id,
            name='End-Sem Viva Assessment',
            exam_type='Viva',  #
            start_date=today + timedelta(days=10),
            end_date=today + timedelta(days=20),
            slot_creation_start=today + timedelta(days=1),
            slot_creation_end=today + timedelta(days=5),
            slot_booking_start=today + timedelta(days=6),
            slot_booking_end=today + timedelta(days=9),
            status='Slot Creation',  #
        ),
        # Completed Exam (Past)
        Examination(
            course_id=course.id,
            name='Project Demo Evaluation',
            exam_type='Project Demo',  #
            start_date=today - timedelta(days=30),
            end_date=today - timedelta(days=20),
            slot_creation_start=today - timedelta(days=45),
            slot_creation_end=today - timedelta(days=40),
            slot_booking_start=today - timedelta(days=39),
            slot_booking_end=today - timedelta(days=31),
            status='Completed',  #
        ),
    ]

    # 3. Database session mein add karke save (commit) karna
    db.session.add_all(dummy_exams)
    db.session.commit()

    print('Dummy examination data inserted successfully!')


if __name__ == '__main__':
  seed_examinations()