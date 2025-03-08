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
        # is_admin = request.form.get('is_admin')
        user = User.query.filter_by(email=email, password = password)
        # is_admin = User.query.filter_by(is_admin = is_admin)
        # if user and user.is_admin == 0:    
        #     return render_template("admin_dashboard.html")
        # elif user and user.is_admin == 1:
        #     return render_template("user_dashboard.html")
        # else:
        #     return render_template('login.html' ,msg = "Invalid user")
        return redirect(url_for("admin_dashboard"))

    


    return render_template('login.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        qualification = request.form.get('qualification')
        is_admin = request.form.get('is_admin')
        dob = request.form.get('DOB')


        dob_str = datetime.strptime(dob, "%Y-%m-%d").date()

        user = User(email=email, password=password, full_name=full_name, qualification=qualification, is_admin = is_admin,dob=dob_str)
        db.session.add(user)
        db.session.commit()

    return render_template('register.html')

@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

if __name__ == '__main__':
    app.run(debug=True)

