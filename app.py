from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

from models import db, User, Subject, Chapter, Quiz, Question, Score
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
                return redirect(url_for('user_dashboard', user_id=user.id))
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


@app.route('/delete_subject')
def delete_subject():
    id = request.args.get('id')
    if id:
        subject = Subject.query.get(id)
        if subject:
            # Delete associated chapters first
            Chapter.query.filter_by(subject_id=id).delete()
            # Then delete the subject
            db.session.delete(subject)
            db.session.commit()
            return redirect(url_for("admin_dashboard"))
        else:
            return "Subject not found", 404
    return "Invalid request", 400


#CRUD operation on Chapter


#Add new chapter "/add_chapter"
@app.route("/add_chapter", methods=["GET", "POST"])
def add_chapter():
    # Get subject_id from URL parameters
    subject_id = request.args.get('subject_id')
    
    if request.method == 'POST':
        # Create new chapter with form data
        new_chapter = Chapter(
            name=request.form.get('name'),
            description=request.form.get('description'),
            # no_of_question=request.form.get('no_of_question'),
            subject_id=request.form.get('subject_id')  # From hidden input
        )
        db.session.add(new_chapter)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    
    # GET request handling
    if not subject_id:
        return redirect(url_for('admin_dashboard'))
    
    # Get subject for display
    subject = Subject.query.get(subject_id)
    if not subject:
        return redirect(url_for('admin_dashboard'))
    
    return render_template('add_chapter.html', subject=subject)


# "/edit_chapter/chapters?id={c.id}"
@app.route("/edit_chapter", methods=["GET", "POST"])
def edit_chapter():
    chapter_id = request.args.get('id')
    chapter = Chapter.query.get_or_404(chapter_id)
    
    if request.method == 'POST':
        chapter.name = request.form.get('name')
        chapter.description = request.form.get('description')
        # chapter.no_of_question = request.form.get('no_of_question')
        chapter.subject_id = request.form.get('subject_id')
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    
    subjects = Subject.query.all()
    return render_template('edit_chapter.html', 
                         chapter=chapter,
                         subjects=subjects)

# "/delete_chapter/chapters?id={c.id}"
@app.route('/delete_chapter')
def delete_chapter():
    id = request.args.get('id')
    if id:
        Quiz.query.filter_by(Chapter_id=id).delete()
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


@app.route("/delete_quiz")
def delete_quiz():
    id = request.args.get('id')
    if id:
        quiz = Quiz.query.get(id)
        if quiz:
            # Delete associated Question first
            Question.query.filter_by(quiz_id=id).delete()
            # Then delete the quiz
            db.session.delete(quiz)
            db.session.commit()
            return redirect(url_for("admin_dashboard"))
        else:
            return "Subject not found", 404
    return "Invalid request", 400

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


@app.route("/user_dashboard/<int:user_id>")
def user_dashboard(user_id):
    user = User.query.get_or_404(user_id)
    quizzes = Quiz.query.all()
    return render_template('user_dashboard.html', quizzes=quizzes, user=user)


@app.route("/view_quiz/<int:quiz_id>/<int:user_id>")
def view_quiz(quiz_id, user_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    user = User.query.get_or_404(user_id)
    return render_template('view_quiz.html', quiz=quiz, user = user)


@app.route("/start_quiz/<int:quiz_id>/<int:user_id>", methods=['GET', 'POST'])
def start_quiz(quiz_id, user_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        score = 0
        for question in quiz.question:
            answer = request.form.get(f'q{question.id}')
            if answer and int(answer) == question.correct_option:
                score += 1
                
        new_score = Score(
            user_id=user_id,
            quiz_id=quiz_id,
            score=score
        )
        db.session.add(new_score)
        db.session.commit()
        
        return redirect(url_for('score', user_id=user_id))
    
    return render_template('start_quiz.html', quiz=quiz, user=user)






#                                            Score of user

@app.route("/scores/<int:user_id>")
def score(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('score.html', user=user)



if __name__ == '__main__':
    app.run(debug=True)

