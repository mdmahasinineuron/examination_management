from flask import Flask, render_template, request
from extensions import db
from models import User

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
        if request.form['email'] == 'admin@gmail.com':
            return render_template('admin/dashboard.html')
        if request.form['email'] == 'student@gmail.com':
            return render_template('student/dashboard.html')
        if request.form['email'] == 'examinar@gmail.com':
            return render_template('examinar/dashboard.html')

    return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)