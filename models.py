from app import db
from flask_login import UserMixin
from datetime import datetime

# 1. User Table (Authentication & Role Management)
# Admin, Examiner, aur Student teeno yahi se login karenge[cite: 5]
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Allowed values: 'admin', 'examiner', 'student'

# 2. Examiner Profile Table[cite: 9]
# Extra details sirf Examiners ke liye. (Admin inko approve/deactivate karega)
class ExaminerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    department = db.Column(db.String(100))
    contact_details = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Pending') # 'Pending', 'Approved', 'Deactivated'[cite: 3]

# 3. Course Table[cite: 6]
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Active')

# 4. Examination Table[cite: 6, 7]
class Examination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    exam_type = db.Column(db.String(50), nullable=False) # 'Viva', 'Practical', 'Project Demo', 'Assessment'[cite: 6]
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    slot_creation_start = db.Column(db.Date, nullable=False)
    slot_creation_end = db.Column(db.Date, nullable=False)
    slot_booking_start = db.Column(db.Date, nullable=False)
    slot_booking_end = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='Draft') # 'Draft', 'Slot Creation', 'Booking Open', 'Closed', 'Completed'[cite: 7]

# 5. Examination Rubric Table[cite: 7]
# Examiner marks dete time in criteria ko use karega
class Rubric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    examination_id = db.Column(db.Integer, db.ForeignKey('examination.id'), nullable=False)
    criterion_name = db.Column(db.String(100), nullable=False)
    max_marks = db.Column(db.Integer, nullable=False)
    weightage = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)

# 6. Examination Slot Table[cite: 8]
class ExaminationSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    examination_id = db.Column(db.Integer, db.ForeignKey('examination.id'), nullable=False)
    examiner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Available') # 'Available', 'Full', 'Cancelled', 'Completed'[cite: 8]

# 7. Booking Table[cite: 8, 9]
# Student ka slot book hone ka record
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('examination_slot.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Booked') # 'Booked', 'Cancelled', 'Completed'[cite: 9]