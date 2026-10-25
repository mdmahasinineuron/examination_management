from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from datetime import date, datetime
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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin/courses/add', methods=['POST'])
def add_course():
    # Access Control: Sirf admin add kar sakta hai
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    # HTML form se name attributes ke through data nikalna
    form_course_code = request.form.get('course_code')
    form_course_name = request.form.get('course_name')

    # Agar user ne dono details daali hain
    if form_course_code and form_course_name:
        # Naya Course object banana
        new_course = Course(
            course_code=form_course_code, 
            course_name=form_course_name
        )
        
        courses = Course.query.all()
        course_code = []
        for course in courses:
            course_code.append(course.course_code)
            
        
        # Database mein save karna
        if form_course_code not in course_code:
            db.session.add(new_course)
            db.session.commit()
            flash(f"Success: '{form_course_code}' New corse added successfully", "success")
        else:
            flash(f"Course {form_course_code} already exist", "danger")

    # Wapas courses page par bhej dena jahan naya data automatically dikhega
    return redirect(url_for('admin_courses'))

@app.route('/admin/courses/delete/<int:id>')
def delete_course(id):
    # 1. Jo ID URL se aayi hai, usse database mein dhoondho
    course_to_delete = Course.query.get(id)
    
    # 2. Agar course mil gaya, toh usko table se mita do
    if course_to_delete:
        db.session.delete(course_to_delete)
        db.session.commit()
        flash(f"Course {course_to_delete.course_name} has been deleted", "success")
    else:
        # Agar koi aisi ID bhej de jo database mein hai hi nahi
        flash("Error: Course database mein nahi mila.", "danger")
        
    # 3. Wapas courses table wale page par bhej do
    return redirect(url_for('admin_courses'))


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
                         total_bookings=total_bookings,total_exams=total_exams,Courselist=Courselist)

@app.route('/admin/courses')
def admin_courses():
    courses = Course.query.all()
    return render_template('admin/courses.html', active_page='courses', courses=courses)

@app.route('/admin/exams')
def admin_exams():
    exams = Examination.query.all()
    courses = Course.query.all()
    return render_template('admin/exams.html', active_page='exams', exams=exams,courses=courses)

@app.route('/admin/exams/add', methods=['POST'])
def add_exam():
    course_code = request.form.get('course_code')
    exam_name = request.form.get('exam_name')
    exam_type = request.form.get('exam_type')
    exam_start_date=datetime.strptime(request.form.get('exam_start_date'), '%Y-%m-%d').date()
    exam_end_date=datetime.strptime(request.form.get('exam_end_date'), '%Y-%m-%d').date()
    slot_start_date= datetime.strptime(request.form.get('slot_start_date'), '%Y-%m-%d').date()
    slot_end_date=datetime.strptime(request.form.get('slot_end_date'),'%Y-%m-%d').date()
    booking_start_date=datetime.strptime(request.form.get('booking_start_date'),'%Y-%m-%d').date()
    booking_end_date=datetime.strptime(request.form.get('booking_end_date'),'%Y-%m-%d').date()
    
    if (exam_start_date>exam_end_date) or (slot_start_date>slot_end_date) or (booking_start_date>booking_end_date):
      flash("Error: Start date cannot be after end date please check dates carefully.", "danger")
      return  redirect(url_for('admin_exams'))
    else:
        course_id = int(Course.query.filter_by(course_code=course_code).first().id)
        new_exam = Examination(
            course_id=course_id,  # Form se aayi direct ID
            name=exam_name,
            exam_type=exam_type,
            start_date=exam_start_date,
            end_date=exam_end_date,
            slot_creation_start=slot_start_date,
            slot_creation_end=slot_end_date,
            slot_booking_start=booking_start_date,
            slot_booking_end=booking_end_date,
            status='Draft'
        )
        db.session.add(new_exam)
        db.session.commit()
        flash("Success: Examination created successfully!", "success")
    return redirect(url_for('admin_exams'))
    

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