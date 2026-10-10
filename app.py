from flask import Flask, render_template, request

app = Flask(__name__)






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
    app.run(debug=True)
