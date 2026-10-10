from flask import Flask, render_template, request
from extensions import db
from models import User
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exam_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database ko app ke sath initialize karna
db.init_app(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        
        # getting id password from login page2
        imput_email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=imput_email).first()
        
        # Authonication
        if user and user.password == password:
            
            if user.role == 'admin':
                return render_template('admin/dashboard.html')
            
            if user.role == 'examinar':
                return render_template('examiner/dashboard.html')
            
            if user.role == 'student':
                return render_template('student/dashboard.html')

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