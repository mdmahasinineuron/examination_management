from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import date
from extensions import db
from models import (
    Booking,
    Course,
    Examination,
    ExaminationSlot,
    ExaminerProfile,
    Rubric,
    User,
)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-fallback-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exam_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
def admin_dashboard():
  if 'user_id' not in session:
    return redirect(url_for('login'))
 
  if session.get('role') != 'admin':
    return 'Unauthorized Access! Only admins allowed.', 403

  total_courses = Course.query.count()
  total_examinars = User.query.filter_by(role='examiner').count()
  total_exams = Examination.query.count()
  total_student = User.query.filter_by(role='student').count()
  total_slots = ExaminationSlot.query.count()
  total_bookings = Booking.query.count()
  Courselist = Course.query.all()
  return render_template('admin/dashboard.html', total_courses=total_courses, total_exam=total_examinars,
                         total_examinars=total_examinars,total_student=total_student,total_slots=total_slots,
                         total_bookings=total_bookings)

@app.route('/admin/courses')
def admin_courses():
    courses = Course.query.all()
    return render_template('admin/courses.html', active_page='courses', courses=courses)

@app.route('/admin/exams')
def admin_exams():
    return render_template('admin/exams.html', active_page='exams')

@app.route('/admin/rubrics')
def admin_rubrics():
    return render_template('admin/rubrics.html', active_page='rubrics')

@app.route('/admin/examiners')
def admin_examiners():
    return render_template('admin/examiners.html', active_page='examiners')

@app.route('/admin/slots')
def admin_slots():
    return render_template('admin/slots.html', active_page='slots')

@app.route('/admin/bookings')
def admin_bookings():
    return render_template('admin/bookings.html', active_page='bookings')
    
@app.route('/admin/directory')
def admin_directory():
    return render_template('admin/directory.html', active_page='directory')


@app.route('/', methods=['GET', 'POST'])
def login():
  if 'user_id' in session:
    if session.get('role') == 'admin':
      return redirect(url_for('admin_dashboard'))
    elif session.get('role') == 'examiner':
      return redirect(url_for('examiner_dashboard'))
    elif session.get('role') == 'student':
      return redirect(url_for('student_dashboard'))

  if request.method == 'POST':
    input_email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=input_email).first()

    if user and user.password == password:
      session['user_id'] = user.id
      session['role'] = user.role

      if user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
      elif user.role == 'examiner':
        return redirect(url_for('examiner_dashboard'))
      elif user.role == 'student':
        return redirect(url_for('student_dashboard'))
      else:
        return 'Invalid Role Assigned!', 403

    return render_template(
        'login.html', error='Invalid Email or Password! Try again.'
    )

  return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # reading admin email and password from .env file
        admin_email = os.getenv('ADMIN_EMAIL')
        admin_password = os.getenv('ADMIN_PASSWORD')
        
        # safely adding default admin using .env variables
        if admin_email and not User.query.filter_by(email=admin_email).first():
            new_admin = User(
                name='Admin',
                email=admin_email,          # .env wala email use karo
                password=str(admin_password), # Password hamesha String hona chahiye
                role='admin',
            )
            db.session.add(new_admin)
            db.session.commit()
            print("Default Admin Created Successfully!")
            
    app.run(debug=True)