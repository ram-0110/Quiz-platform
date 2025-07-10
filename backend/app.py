from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    send_file,
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_cors import CORS
import uuid
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,create_refresh_token
from functools import wraps
import redis
from flask_redis import FlaskRedis

# -------------------------------  App  -----------------------------------------------

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your_secret_key_here"
app.config['JWT_SECRET_KEY'] = 'super-secret' 
app.config['REDIS_URL'] = "redis://localhost:6379/0"  # Default Redis URL

# JWT Configuration for handling CORS
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)


jwt = JWTManager(app)
redis_client = FlaskRedis(app)

# Configure CORS properly - more permissive for development
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

db = SQLAlchemy(app)

# -------------------------------  Database  -----------------------------------------------

# Association table for many-to-many between Users and Subjects
user_subject = db.Table(
    'user_subject',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    attempts = db.relationship('Score', backref='user', lazy=True)
    subjects = db.relationship('Subject', secondary=user_subject, back_populates='students')

class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)

    chapters = db.relationship('Chapter', backref='subject', lazy=True)
    students = db.relationship('User', secondary=user_subject, back_populates='subjects')

class Chapter(db.Model):
    __tablename__ = 'chapters'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)

    quizzes = db.relationship('Quiz', backref='chapter', lazy=True)

class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    quiz_name = db.Column(db.String(120), unique=True, nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    date_of_quiz = db.Column(db.Date, default=datetime.utcnow)
    time_duration = db.Column(db.String(5))
    remarks = db.Column(db.Text)

    questions = db.relationship('Question', backref='quiz', lazy=True)
    attempts = db.relationship('Score', backref='quiz', lazy=True)

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255))
    option4 = db.Column(db.String(255))
    correct_option = db.Column(db.Integer, nullable=False)  # '1','2','3','4'

class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    total_score = db.Column(db.Integer)
    remarks = db.Column(db.Text)

# Create tables
with app.app_context():
    db.create_all()


def is_rate_limited(key, limit, period):
    if redis_client.exists(key):
        count = int(redis_client.get(key))
        if count >= limit:
            return True
        redis_client.incr(key)
        return False
    else:
        redis_client.setex(key, period, 1)
        return False
    
# --------------------------------------------------------------------------------
# Add OPTIONS method handler for routes that need preflight requests
@app.route('/api/login', methods=['OPTIONS'])
def login_options():
    return '', 200

@app.route('/api/signup', methods=['OPTIONS'])
def signup_options():
    return '', 200

@app.route('/api/about', methods=['OPTIONS'])
def about_options():
    return '', 200

@app.route('/api/home', methods=['OPTIONS'])
def home_options():
    return '', 200

# --------------------------------------------------------------------------------
@app.route('/api/signup', methods=['POST'])
def signup():
    ip_key = f"signup_ip:{request.remote_addr}"
    if is_rate_limited(ip_key, 5, 60):
        return jsonify({'error': 'Too many requests'}), 429
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    confirmPassword = data.get('confirmPassword')
    email = data.get('email')
    userid = str(uuid.uuid4())

    user = User.query.filter_by(username=username).first()
    email_user = User.query.filter_by(email=email).first()

    

    if not username or not password or not confirmPassword or not email:
        return jsonify({'message': 'All fields are required', 'error': 'All fields are required'}), 400

    if user:
        return jsonify({'message': 'Username already exists', 'error': 'Username already exists'}), 400

    if email_user:
        return jsonify({'message': 'Email already exists', 'error': 'Email already exists'}), 400

    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters long', 'error': 'password_too_short'}), 400

    if password != confirmPassword:
        return jsonify({'message': 'Passwords do not match', 'error': 'passwords_do_not_match'}), 400
    
    # Hash the password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    # Create a new user
    new_user = User(id=userid, username=username, password=hashed_password, email=email, is_admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201
# --------------------------------------------------------------------------------
@app.route('/api/login', methods=['POST'])
def login():
    ip_key = f"login_ip:{request.remote_addr}"
    if is_rate_limited(ip_key, 10, 60):
        return jsonify({'error': 'Too many requests'}), 429
    
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # ✅ Static Admin Login
    if email == 'admin@gmail.com' and password == 'admin':
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'username': 'admin'
        }), 200

    # ✅ Normal user from database
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'username': user.email
    }), 200

# --------------------------------------------------------------------------------
@app.route('/api/dashboard')
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    cache_key = f"dashboard_{current_user}"
    
    # Check if cached data exists
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return jsonify(json.loads(cached_data)), 200

    user = User.query.filter_by(email=current_user).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Get all subjects from DB
    all_subjects = Subject.query.all()
    subject_list = [
        {"id": subject.id, "name": subject.name}
        for subject in all_subjects
    ]

    response_data = {
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'subjects': subject_list
    }

    # Cache the response for 5 minutes (300 seconds)
    redis_client.setex(cache_key, 300, json.dumps(response_data))
    
    return jsonify(response_data), 200

# --------------------------------------------------------------------------------

@app.route('/api/about', methods=['GET'])
@jwt_required()
def about():
    current_user = get_jwt_identity()
    cache_key = f"about_{current_user}"
    
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return jsonify(json.loads(cached_data)), 200
    
    user = User.query.filter_by(email=current_user).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    subject_id = 1

    results = Chapter.query.filter_by(subject_id=subject_id).all()

    results = [
        {
            'id': chapter.id,
            'name': chapter.name,
            'description': chapter.description,
            'quizzes': [
                {
                    'id': quiz.id,
                    'date_of_quiz': quiz.date_of_quiz,
                    'time_duration': quiz.time_duration,
                    'remarks': quiz.remarks
                }
                for quiz in chapter.quizzes
            ]
        }
        for chapter in results
    ]

    formatted_results = []

    for chapter in results:
        chapter_id = chapter['id']
        chapter_name = chapter['name']
        for quiz in chapter['quizzes']:
            formatted_results.append({
                'quiz id': quiz['id'],
                'chapterid': chapter_id,
                'chaptername': chapter_name,
                'dateofquiz': quiz['date_of_quiz'],
                'timeduration': quiz['time_duration']
            })
    print("Results:", formatted_results)

    redis_client.setex(cache_key, 600, json.dumps({
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'hello': 'Hello, this is the about page!',
        'results': formatted_results
    }))

    return jsonify({
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'hello': 'Hello, this is the about page!',
        'results': formatted_results

    }), 200


# --------------------------------------------------------------------------------

def get_unopted_subjects(user_id):
    # Get subject IDs already opted by the user
    opted_subject_ids = (
        db.session.query(user_subject.c.subject_id)
        .filter(user_subject.c.user_id == user_id)
    )

    # Now get subjects that are NOT in the opted list
    unopted_subjects = Subject.query.filter(~Subject.id.in_(opted_subject_ids)).all()
    return unopted_subjects

def serialize_subject_with_chapters_and_counts(subject):
    chapter_names = [chapter.name for chapter in subject.chapters]
    quiz_count = sum(len(chapter.quizzes) for chapter in subject.chapters)

    return {
        "name": subject.name,
        "topics": chapter_names,
        "chapter_count": len(chapter_names),
        "quiz_count": quiz_count
    }

# --------------------------------------------------------------------------------
@app.route('/api/home')
@jwt_required()
def home():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    cache_key = f"home_{current_user}"
    
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return jsonify(json.loads(cached_data)), 200

    if not user:
        return jsonify({'message': 'User not found'}), 404

    scores_data = []
    for score in user.attempts:  # ← this is valid because of your existing relationship
        quiz = score.quiz
        chapter = quiz.chapter
        subject = chapter.subject

        scores_data.append({
            'score_id': score.id,
            'total_score': score.total_score,
            'timestamp': score.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'quiz': {
                'quiz_id': quiz.id,
                'quiz_name': quiz.quiz_name,
                'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d'),
            },
            'chapter': {
                'chapter_id': chapter.id,
                'chapter_name': chapter.name,
            },
            'subject': {
                'subject_id': subject.id,
                'subject_name': subject.name,
            }
        })

    redis_client.setex(cache_key, 180, json.dumps({
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'scores': scores_data,
    }))
    
    return jsonify({
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'scores': scores_data,
    }), 200

# --------------------------------------------------------------------------------
@app.route('/api/dashboard-sub-quiz')
@jwt_required()
def dashboard_sub_quiz():
    current_user = get_jwt_identity()
    subject_id = request.args.get('subjectid') 
    user = User.query.filter_by(email=current_user).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Get quiz_ids already attempted by the user
    attempted_quiz_ids = {score.quiz_id for score in user.attempts}

    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    formatted_results = []

    for chapter in chapters:
        for quiz in chapter.quizzes:
            if quiz.id not in attempted_quiz_ids:
                formatted_results.append({
                    'quiz_id': quiz.id,
                    'chapterid': chapter.id,
                    'chaptername': chapter.name,
                    'dateofquiz': quiz.date_of_quiz,
                    'timeduration': quiz.time_duration,
                    'remarks': quiz.remarks
                })

    return jsonify(results=formatted_results), 200

# --------------------------------------------------------------------------------
@app.route('/api/add-subject', methods=['POST'])
@jwt_required()
def add_subject():
    data = request.get_json()
    subjectname=data.get("subjectName")

    new_subject=Subject(name=subjectname)
    db.session.add(new_subject)
    db.session.commit()

    return jsonify({"message": "Subject added successfully"}), 200

# --------------------------------------------------------------------------------
@app.route('/api/add-stu-sub',methods=['POST'])
@jwt_required()
def link_stu_sub():
    data = request.get_json()
    subjectname = data.get("name")
    current_user = get_jwt_identity()

    user = User.query.filter_by(email=current_user).first()
    subject = Subject.query.filter_by(name=subjectname).first()

    if not user or not subject:
        return jsonify({"error": "No user or subject found"}), 404

    if subject not in user.subjects:
        user.subjects.append(subject)
        db.session.commit()

    return jsonify({"message": "subject added successfully"}), 200



@app.route('/api/add-chapter', methods=['POST'])
@jwt_required()
def add_chapter():
    data = request.get_json()
    subjectname = data.get("subjectName")
    chaptername = data.get("chapterName")
    subject = Subject.query.filter_by(name=subjectname).first()

    print(subjectname, chaptername)

    if not subject:
        return jsonify({"message": "Subject not found"}), 404

    new_chapter = Chapter(name=chaptername, subject_id=subject.id)
    db.session.add(new_chapter)
    db.session.commit()


    

    return jsonify({"message": "Chapter added successfully"}), 200

# --------------------------------------------------------------------------------
@app.route('/api/subjects-chapters-admin', methods=['GET'])
@jwt_required()
def get_subjects_chapters_admin():
    subjects = Subject.query.all()
    subjects_data = []

    for subject in subjects:
        chapters = Chapter.query.filter_by(subject_id=subject.id).all()
        topics = [chapter.name for chapter in chapters]
        subjects_data.append({
            'name': subject.name,
            'topics': topics
        })

    print("Subjects and Chapters Data:", subjects_data)

    return jsonify({'subjects': subjects_data}), 200

# --------------------------------------------------------------------------------
def sort_and_join(arr):
    # Safely sort and join elements as strings
    return ''.join(sorted(map(str, arr)))

@app.route('/api/add-quizzes', methods=['POST'])
@jwt_required()
def add_quizzes():
    current_user = get_jwt_identity()
    data = request.get_json()

    # Validate input
    subject_name = data.get("subject")
    chapter_name = data.get("chapter")
    quiz_name = data.get("quiz")
    problems = data.get("problem")

    if not all([subject_name, chapter_name, quiz_name, problems]):
        return jsonify({'message': 'Missing required fields'}), 400

    print("Subject:", subject_name)
    print("Chapter:", chapter_name)
    print("Quiz Name:", quiz_name)
    print("Problems:", problems)

    # Check subject
    subject = Subject.query.filter_by(name=subject_name).first()
    if not subject:
        return jsonify({'message': 'Subject not found'}), 404

    # Check chapter
    chapter = Chapter.query.filter_by(name=chapter_name, subject_id=subject.id).first()
    if not chapter:
        return jsonify({'message': 'Chapter not found'}), 404

    # Check if quiz already exists
    quiz = Quiz.query.filter_by(quiz_name=quiz_name, chapter_id=chapter.id).first()
    if quiz:
        return jsonify({'message': 'Quiz already exists'}), 400

    # Create new quiz
    new_quiz = Quiz(
        quiz_name=quiz_name,
        chapter_id=chapter.id,
        date_of_quiz=datetime.utcnow(),
        time_duration='10:00'
    )
    db.session.add(new_quiz)
    db.session.commit()

    # Add questions
    for question in problems:
        q_type = question.get('type')
        options = question.get('options')
        q_text = question.get('question')

        if q_type not in ['single-choice', 'multiple-choice'] or not options or not q_text:
            continue  # Skip invalid questions

        if q_type == 'single-choice':
            correct_option = question.get('correctOption')

        elif q_type == 'multiple-choice':
            correct_options = question.get('correctOptions', [])
            correct_option = sort_and_join(correct_options)

        new_question = Question(
            quiz_id=new_quiz.id,
            question_statement=q_text,
            option1=options[0],
            option2=options[1],
            option3=options[2],
            option4=options[3],
            correct_option=correct_option
        )
        db.session.add(new_question)

    db.session.commit()

    return jsonify({'message': 'Quiz added successfully'}), 201

# --------------------------------------------------------------------------------


@app.route('/api/update-quiz', methods=['POST'])
@jwt_required()
def update_quiz():
    current_user = get_jwt_identity()
    data = request.get_json()

    # Extract data
    subject_name = data.get("subject")
    chapter_name = data.get("chapter")
    quiz_name = data.get("quiz")
    problems = data.get("problem")

    if not all([subject_name, chapter_name, quiz_name, problems]):
        return jsonify({'message': 'Missing required fields'}), 400

    print("Updating quiz for:", subject_name, chapter_name, quiz_name)

    # Validate subject
    subject = Subject.query.filter_by(name=subject_name).first()
    if not subject:
        return jsonify({'message': 'Subject not found'}), 404

    # Validate chapter
    chapter = Chapter.query.filter_by(name=chapter_name, subject_id=subject.id).first()
    if not chapter:
        return jsonify({'message': 'Chapter not found'}), 404

    # Find existing quiz
    quiz = Quiz.query.filter_by(quiz_name=quiz_name, chapter_id=chapter.id).first()
    if not quiz:
        return jsonify({'message': 'Quiz not found'}), 404

    # Optional: update quiz metadata
    quiz.date_of_quiz = datetime.utcnow()  # or leave unchanged
    db.session.commit()

    # Clear old questions
    Question.query.filter_by(quiz_id=quiz.id).delete()

    # Add new questions
    for question in problems:
        q_type = question.get('type')
        q_text = question.get('question')
        options = question.get('options')

        if q_type not in ['single-choice', 'multiple-choice'] or not q_text or not options:
            continue

        if q_type == 'single-choice':
            correct_option = question.get('correctOption')
        else:
            correct_options = question.get('correctOptions', [])
            correct_option = sort_and_join(correct_options)

        new_question = Question(
            quiz_id=quiz.id,
            question_statement=q_text,
            option1=options[0],
            option2=options[1],
            option3=options[2],
            option4=options[3],
            correct_option=correct_option
        )
        db.session.add(new_question)

    db.session.commit()

    return jsonify({'message': 'Quiz updated successfully'}), 200

# --------------------------------------------------------------------------------
@app.route('/api/get-quiz-admin', methods=['GET'])
@jwt_required()
def get_quiz_admin():

    chapter_name = request.args.get("chapter")
    print("\n\n\n\n\n\n\n\n\n\n")
    print("Chapter:", chapter_name)


    chapter = Chapter.query.filter_by(name=chapter_name).first()
    if not chapter:
        return jsonify({'message': 'Chapter not found'}), 404
    
    print("Chapter ID:", chapter.id)    

    quizzes = Quiz.query.filter_by(chapter_id=chapter.id).all()
    quiz_data = []

    for quiz in quizzes:
        quiz_data.append({
            "id": quiz.id,
            "type": chapter.name,
            "description": quiz.quiz_name,
            "status": quiz.time_duration,
            "priority": quiz.date_of_quiz,
            "selected": "false",
        })

    print("Quiz Data:", quiz_data)
    return jsonify(quiz_data), 200

# --------------------------------------------------------------------------------

@app.route('/api/get-quiz', methods=['GET'])
def get_quiz():
    quiz_id = request.args.get('id')
    quiz= Quiz.query.filter_by(id=quiz_id).first()
    print("Quiz ID:", quiz_id)
    
    
    # Replace with actual quiz logic


    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404

    chapter = Chapter.query.filter_by(id=quiz.chapter_id).first()
    subject = Subject.query.filter_by(id=chapter.subject_id).first()

    print("Chapter ID:", chapter.id)
    print("Subject ID:", subject.id)

    # Build response data
    quiz_data = {
        'quiz': quiz.quiz_name,
        'chapter': chapter.name,
        'subject': subject.name,
        'problem': [
            {
                'question_statement': q.question_statement,
                'option1': q.option1,
                'option2': q.option2,
                'option3': q.option3,
                'option4': q.option4,
                'correct_option': q.correct_option,
            }
            for q in quiz.questions
        ]
    }

    print("Quiz Data:", quiz_data)


    return jsonify(quiz_data), 200


# --------------------------------------------------------------------------------
@app.route('/api/dashboard-cardnum', methods=['GET'])
@jwt_required()
def dashboard_card_num():
    quiz_id = request.args.get('id')

    quiz = Quiz.query.filter(Quiz.id == quiz_id).first()

    quiz_data = {
        'quiz_name': quiz.quiz_name,
        'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d'),  # convert date to string
        'time_duration': quiz.time_duration,
        'chapter_id': quiz.chapter_id,
    }
    

    return jsonify({
        'message':'eveything okay',
        'quiz_data':quiz_data,
    }), 200

# --------------------------------------------------------------------------------
@app.route('/api/quiz/<int:quiz_id>')
@jwt_required()
def get_quiz_by_id(quiz_id):
    quiz = Quiz.query.get(quiz_id)

    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404

    chapter = quiz.chapter
    subject = chapter.subject

    return jsonify({
        'id': quiz.id,
        'quiz_name': quiz.quiz_name,
        'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d'),
        'time_duration': quiz.time_duration,
        'remarks': quiz.remarks,

        'chapter': {
            'id': chapter.id,
            'name': chapter.name,
            'description': chapter.description
        },

        'subject': {
            'id': subject.id,
            'name': subject.name,
            'description': subject.description
        },

        'message': 'done'
    })

# --------------------------------------------------------------------------------
@app.route('/api/quiz/start/<int:quiz_id>',methods=['GET'])
@jwt_required()
def start_quiz(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    quiz=Quiz.query.filter_by(id=quiz_id).first()
    print(quiz.time_duration)
    if not questions:
        return jsonify({"message": "No questions found for this quiz"}), 404

    question_list = []
    for q in questions:
        question_list.append({
            "id": q.id,
            "question_statement": q.question_statement,
            "option1": q.option1,
            "option2": q.option2,
            "option3": q.option3,
            "option4": q.option4,
            "correct_option": q.correct_option,
            'time':quiz.time_duration,
        })

    return jsonify(question_list), 200


@app.route('/api/quiz/submit/<int:quiz_id>/result', methods=['POST', 'OPTIONS'])
@jwt_required(optional=True)  # optional=True allows OPTIONS without auth
def submit_quiz(quiz_id):
    if request.method == 'OPTIONS':
        return jsonify({'ok': True}), 200  # respond to preflight

    current_user_email = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'answers' not in data:
        return jsonify({"error": "Missing answers"}), 400

    # Fetch user
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    existing_score = Score.query.filter_by(quiz_id=quiz_id, user_id=user.id).first()
    if existing_score:
        return jsonify({"message": "You have already submitted this quiz."}), 409


    answers = data['answers']
    score = 0

    for ans in answers:
        question_id = ans.get('question_id')
        selected_option = ans.get('selected_option')
        if selected_option is None:
            continue  # skip unanswered questions

        question = db.session.get(Question, question_id)
        if question and question.correct_option == selected_option:
            score += 1

    # Store the score
    new_score = Score(
        quiz_id=quiz_id,
        user_id=user.id,
        total_score=score,
        remarks=f"Scored {score} out of {len(answers)}"
    )
    db.session.add(new_score)
    db.session.commit()

    print(score)
    return jsonify({
        "message": "Quiz submitted successfully!",
        "score": score,
        "total_questions": len(answers)
    }), 200


@app.route('/api/quiz/result/<int:quiz_id>', methods=['GET'])
@jwt_required(optional=True) 
def get_quiz_result(quiz_id):
    user_id = get_jwt_identity()  # or your user authentication system
    user = User.query.filter_by(email=user_id).first()
    print(user.id)
    score = Score.query.filter_by(quiz_id=quiz_id, user_id=user.id).first()
    if not score:
        return jsonify({'message': 'Result not found'}), 404

    return jsonify({
        'quiz_id': score.quiz_id,
        'quiz_name': score.quiz.quiz_name,
        'total_score': score.total_score,
        'remarks': score.remarks,
        'timestamp': score.timestamp.isoformat()
    }), 200

@app.route('/api/stats/static', methods=['GET'])
@jwt_required()
def get_static_stats():
    user_mail = get_jwt_identity()
    user = User.query.filter_by(email=user_mail).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_id = user.id

    # 1. Quiz-wise score (scored vs total)
    quiz_scores = (
        db.session.query(
            Quiz.id,
            Quiz.quiz_name,
            Score.total_score,
            db.func.count(Question.id).label('total_marks')
        )
        .join(Score, Quiz.id == Score.quiz_id)
        .join(Question, Quiz.id == Question.quiz_id)
        .filter(Score.user_id == user_id)
        .group_by(Quiz.id, Score.total_score)
        .all()
    )
    quiz_wise = [
        {
            "quiz_id": qid,
            "quiz_name": name,
            "scored": score,
            "total_marks": total,
            "percentage": round((score / total) * 100, 2) if total else 0,
            "chapter_id": Quiz.query.get(qid).chapter_id 

        }
        for qid, name, score, total in quiz_scores
    ]

    # 2. Chapter-wise stats (scored, total marks, attempted vs total quizzes)
    chapters = Chapter.query.all()
    chapter_wise = []
    for chapter in chapters:
        quizzes = chapter.quizzes
        total_quizzes = len(quizzes)
        attempted = 0
        total_score = 0
        total_possible = 0

        for quiz in quizzes:
            score_entry = Score.query.filter_by(quiz_id=quiz.id, user_id=user_id).first()
            question_count = Question.query.filter_by(quiz_id=quiz.id).count()
            total_possible += question_count

            if score_entry:
                attempted += 1
                total_score += score_entry.total_score

        chapter_wise.append({
            "chapter_id": chapter.id,
            "chapter_name": chapter.name,
            "scored": total_score,
            "subject_id": chapter.subject_id,
            "percentage": round((total_score / total_possible) * 100, 2) if total_possible else 0,
            "total_marks": total_possible,
            "attempted_quizzes": attempted,
            "total_quizzes": total_quizzes
        })

    # 3. Subject-wise stats (scored, total marks, attempted vs total quizzes)
    subjects = Subject.query.all()
    subject_wise = []
    for subject in subjects:
        chapters = subject.chapters
        total_quizzes = 0
        attempted = 0
        total_score = 0
        total_possible = 0

        for chapter in chapters:
            for quiz in chapter.quizzes:
                total_quizzes += 1
                score_entry = Score.query.filter_by(quiz_id=quiz.id, user_id=user_id).first()
                question_count = Question.query.filter_by(quiz_id=quiz.id).count()
                total_possible += question_count

                if score_entry:
                    attempted += 1
                    total_score += score_entry.total_score

        subject_wise.append({
            "subject_id": subject.id,
            "subject_name": subject.name,
            "scored": total_score,
            "total_marks": total_possible,
            "attempted_quizzes": attempted,
            "total_quizzes": total_quizzes
        })

    return jsonify({
        "quiz_wise": quiz_wise,
        "chapter_wise": chapter_wise,
        "subject_wise": subject_wise
    })




if __name__ == "__main__":
    app.run(debug=True)