from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from models import db, User, Subject, Chapter, Quiz, Question
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

@app.route("/admin_dashboard", methods = ['GET', 'POST'])
def admin_dashboard():
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    return render_template("admin_dashboard.html", subjects = subjects, chapters = chapters )




#Add Subject

@app.route("/add_subject",methods = ['GET', "POST"])
def add_subject():
    if request.method =='POST':
        name = request.form.get('name')
        description = request.form.get('description')
        s = Subject(name = name, description = description)
        db.session.add(s)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('add_subject.html')

#CRUD operation on Chapter
#Add new chapter "/add_chapter"
@app.route("/add_chapter", methods = ["POST"])
def add_chapter():
    if request.method =='POST':
        name = request.form.get('name')
        description = request.form.get('description')
        no_of_question = request.form.get('no_of_question')
        subject_id = request.form.get('subject_id')
        c = Chapter(name = name, description = description, no_of_question = no_of_question, subject_id = subject_id)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('add_chapter.html')



# "/edit_chapter/chapters?id={c.id}"
# "/delete_chapter/chapters?id={c.id}"
@app.route('/delete_chapter')
def delete_chapter():
    id = request.args.get('id')
    if id:
        obj = Chapter.query.filter_by(id=id).first()
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return redirect(url_for("admin_dashboard"))
        else:
            return "Chapter not found", 404
    return "Invalid request", 400


if __name__ == '__main__':
    app.run(debug=True)

