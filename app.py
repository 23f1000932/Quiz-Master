from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from models import db, User
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db.init_app(app)
app.app_context().push()
db.create_all()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email)
        if user:
            return render_template("user_dashboard.html")
        else:
            # Handle the case where the user is not found
            return render_template('login.html')
    


    return render_template('login.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        qualification = request.form.get('qualification')
        # is_admin = request.form.get('is_admin')
        dob = request.form.get('DOB')

# Convert DOB to string
        dob_str=request.form.get("dob")
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()

        user = User(email=email, password=password, full_name=full_name, qualification=qualification, dob=dob_str)
        db.session.add(user)
        db.session.commit()

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

