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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, password = password).first()

        if user:
            if user.email == "ayanhussain4212@gmail.com":
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            return render_template("login.html", msg = "Invalid email or password")
    return render_template('login.html')



@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')


        full_name = request.form.get('full_name')
        qualification = request.form.get('qualification')
        dob = request.form.get('DOB')


        dob_str = datetime.strptime(dob, "%Y-%m-%d").date()

        user = User(email=email, password=password, full_name=full_name, qualification=qualification, dob=dob_str)
        db.session.add(user)
        db.session.commit()

    return render_template('register.html')




#Admin dashboard
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
@app.route("/add_chapter", methods = ["GET","POST"])
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
@app.route("/edit_chapter", methods = ["GET","POST"])
def edit_chapter():
    id = request.args.get('id')
    obj = Chapter.query.filter_by(id=id).first()
    if request.method =='POST':
        obj.name = request.form.get('name')
        obj.description = request.form.get('description')
        obj.no_of_question = request.form.get('no_of_question')
        obj.subject_id = request.form.get('subject_id')
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_chapter.html')


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





#Quiz Management route
@app.route("/quiz_management", methods = ['GET', 'POST'])
def quiz_management():
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    quizzes = Quiz.query.all()
    question = Question.query.all()
    return render_template("quiz_management.html", subjects = subjects, chapters = chapters, quizzes = quizzes, question = question)


#Add Quiz
@app.route("/add_quiz", methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':
        chapter_id = request.form.get('chapter_id')
        remark = request.form.get('remark')
        time_duration = request.form.get('time_duration')
        new_quiz = Quiz(
            chapter_id=chapter_id,
            date_of_quiz=datetime.now().strftime("%Y-%m-%d"),
            remark=remark,
            time_duration = time_duration
        )
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for('quiz_management'))
    chapters = Chapter.query.all()
    return render_template('add_quiz.html', chapters=chapters)

#Add Question
@app.route("/add_question/<int:quiz_id>", methods=['GET', 'POST'])
def add_question(quiz_id):
    if request.method == 'POST':
        new_question = Question(
            quiz_id=quiz_id,
            q_statement=request.form.get('q_statement'),
            o_1=request.form.get('o_1'),
            o_2=request.form.get('o_2'),
            o_3=request.form.get('o_3'),
            o_4=request.form.get('o_4'),
            correct_option=request.form.get('correct_option')
        )
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('quiz_management'))
    return render_template('add_question.html', quiz_id=quiz_id)

#edit Question
@app.route("/edit_question/<int:id>", methods=['GET', 'POST'])
def edit_question(id):
    question = Question.query.get_or_404(id)
    if request.method == 'POST':
        # Update all fields directly from form data
        question.q_statement = request.form['q_statement']
        question.o_1 = request.form['o_1']
        question.o_2 = request.form['o_2']
        question.o_3 = request.form['o_3']
        question.o_4 = request.form['o_4']
        question.correct_option = request.form['correct_option']
        db.session.commit()
        return redirect(url_for('quiz_management'))
    return render_template('edit_question.html', question=question)


#delete Question
@app.route("/delete_question/<int:id>")
def delete_question(id):
    question = Question.query.get_or_404(id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('quiz_management'))




#summary route
@app.route("/admin_summary")
def admin_summary():
    return render_template("admin_summary.html")


@app.route("/user_dashboard")
def user_dashboard():
    return render_template('user_dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)

