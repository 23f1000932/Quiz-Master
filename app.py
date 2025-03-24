from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

from models import db, User, Subject, Chapter, Quiz, Question, Score
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db.init_app(app)
app.app_context().push()
db.create_all()
# / / / / / / / / / / / login and register/ / / / / / / / / / / / 
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



# / / / / / / / / / / /Admin Dashboard/ / / / / / / / / / / / 


#Admin dashboard
@app.route("/admin_dashboard", methods = ['GET', 'POST'])
def admin_dashboard():
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    return render_template("admin_dashboard.html", subjects = subjects, chapters = chapters )


# Admin Dashboard Search
@app.route("/admin_search")
def admin_search():
    search_key = request.args.get('search_key', '').strip().lower()
    filtered_subjects = Subject.query.filter(
        db.or_(
            Subject.name.ilike(f'%{search_key}%'),
            Subject.description.ilike(f'%{search_key}%')
        )
    ).all()
    filtered_chapters = Chapter.query.filter(
        db.or_(
            Chapter.name.ilike(f'%{search_key}%'),
            Chapter.description.ilike(f'%{search_key}%')
        )
    ).all()
    return render_template('admin_dashboard.html',
                         subjects=filtered_subjects,
                         chapters=filtered_chapters,
                         search_key=search_key)


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

# delete_subject
@app.route('/delete_subject')
def delete_subject():
    id = request.args.get('id')
    if id:
        subject = Subject.query.get(id)
        if subject:
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
        obj = Chapter.query.filter_by(id=id).first()
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return redirect(url_for("admin_dashboard"))
        else:
            return "Chapter not found", 404
    return "Invalid request", 400


# / / / / / / / / / / /Quiz management/ / / / / / / / / / / / 




#Quiz Management route
@app.route("/quiz_management", methods = ['GET', 'POST'])
def quiz_management():
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    quizzes = Quiz.query.all()
    question = Question.query.all()
    return render_template("quiz_management.html", subjects = subjects, chapters = chapters, quizzes = quizzes, question = question)


# Quiz Management Search
@app.route("/quiz_search")
def quiz_search():
    search_key = request.args.get('search_key', '').strip().lower()
    filtered_quizzes = Quiz.query.join(Chapter).filter(
        db.or_(
            Quiz.remark.ilike(f'%{search_key}%'),
            Chapter.name.ilike(f'%{search_key}%')
        )
    ).all()
    return render_template('quiz_management.html',
                         subjects=Subject.query.all(),
                         search_key=search_key,
                         filtered_quizzes=filtered_quizzes)


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

#delete Quiz
@app.route("/delete_quiz")
def delete_quiz():
    id = request.args.get('id')
    if id:
        quiz = Quiz.query.get(id)
        if quiz:
            db.session.delete(quiz)
            db.session.commit()
            return redirect(url_for("quiz_management"))
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



# / / / / / / / / / / /User Dashboard/ / / / / / / / / / / / 



@app.route("/user_dashboard/<int:user_id>")
def user_dashboard(user_id):
    user = User.query.get_or_404(user_id)
    quizzes = Quiz.query.all()
    return render_template('user_dashboard.html', quizzes=quizzes, user=user)


# User Dashboard Search
@app.route("/user_search/<int:user_id>")
def user_search(user_id):
    search_key = request.args.get('search_key', '').strip().lower()
    user = User.query.get_or_404(user_id)
    filtered_quizzes = Quiz.query.join(Chapter).filter(
        db.or_(
            Quiz.remark.ilike(f'%{search_key}%'),
            Chapter.name.ilike(f'%{search_key}%')
        )
    ).all()
    return render_template('user_dashboard.html',
                         user=user,
                         quizzes=filtered_quizzes,
                         search_key=search_key)



# view_quiz
@app.route("/view_quiz/<int:quiz_id>/<int:user_id>")
def view_quiz(quiz_id, user_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    user = User.query.get_or_404(user_id)
    return render_template('view_quiz.html', quiz=quiz, user = user)

# start_quiz
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






# / / / / / / / / / / /User Score/ / / / / / / / / / / / 

@app.route("/scores/<int:user_id>")
def score(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('score.html', user=user)


# / / / / / / / / / / /User Summary/ / / / / / / / / / / / 


import matplotlib
matplotlib.use('Agg')  # Required for server environments
import matplotlib.pyplot as plt
import os

@app.route("/user_summary/<int:user_id>")
def user_summary(user_id):
    user = User.query.get_or_404(user_id)
    scores = Score.query.filter_by(user_id=user.id).all()
    if not scores:
        return render_template('user_summary.html', user=user, plot_exists=False)
    # Prepare chart data
    quiz_ids = [f"Quiz {score.quiz.id}" for score in scores]
    user_scores = [score.score for score in scores]
    total_question = [len(score.quiz.question) for score in scores]
    # Create plot
    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    index = range(len(quiz_ids))
    bars1 = plt.bar(index, user_scores, bar_width, label='Your Score', color='#4CAF50')
    bars2 = plt.bar([i + bar_width for i in index], total_question, bar_width, label='Total Questions', color='#2196F3')
    plt.xlabel('Quizzes')
    plt.ylabel('Number of Questions')
    plt.title(f'Quiz Performance for {user.full_name}')
    plt.xticks([i + bar_width/2 for i in index], quiz_ids)
    plt.legend()
    # Add value labels on top of bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                     f'{int(height)}',
                     ha='center', va='bottom')
    # Save plot to static folder
    static_dir = os.path.join(app.root_path, 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    plot_path = os.path.join(static_dir, f'summary_{user_id}.png')
    plt.savefig(plot_path, bbox_inches='tight')
    plt.close()
    return render_template('user_summary.html', 
                         user=user,
                         plot_exists=True,
                         plot_url=url_for('static', filename=f'summary_{user_id}.png'))




# / / / / / / / / / / /Admin Score/ / / / / / / / / / / / 



@app.route("/admin_summary")
def admin_summary():
    # Get all quizzes
    quizzes = Quiz.query.all()
    if not quizzes:
        return render_template("admin_summary.html", plot_exists=False)
    # Prepare data
    quiz_labels = []
    attempt_counts = []
    avg_scores = []
    for quiz in quizzes:
        quiz_labels.append(f"Quiz {quiz.id} ({quiz.chapter.name})")
        # Get all scores for this quiz
        scores = Score.query.filter_by(quiz_id=quiz.id).all()
        attempt_counts.append(len(scores))
        if len(scores) > 0:
            avg = sum([s.score for s in scores]) / len(scores)
        else:
            avg = 0
        avg_scores.append(avg)
    # Create plots
    plt.figure(figsize=(15, 6))
    # Plot 1: Attempt Counts
    plt.subplot(1, 2, 1)
    bars1 = plt.bar(quiz_labels, attempt_counts, color='#FFA500')
    plt.title('Number of Attempts per Quiz')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Number of Users')
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)}',
                 ha='center', va='bottom')
    # Plot 2: Average Scores
    plt.subplot(1, 2, 2)
    bars2 = plt.bar(quiz_labels, avg_scores, color='#008080')
    plt.title('Average Scores per Quiz')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Average Score')
    # Add value labels
    for bar in bars2:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.1f}',
                 ha='center', va='bottom')
    # Save plot
    plt.tight_layout()
    static_dir = os.path.join(app.root_path, 'static')
    plot_path = os.path.join(static_dir, 'admin_summary.png')
    plt.savefig(plot_path, bbox_inches='tight')
    plt.close()
    return render_template('admin_summary.html',
                         plot_exists=True,
                         plot_url=url_for('static', filename='admin_summary.png'))





if __name__ == '__main__':
    app.run(debug=True)

