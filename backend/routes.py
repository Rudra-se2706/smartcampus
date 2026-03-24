import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from security.ai_integration import ask_ai
from flask import render_template, request, redirect, url_for, session, jsonify
from models import db, User, Notice, StudyGroup, LoginAttempt
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt()

def register_routes(app):
    bcrypt.init_app(app)

    # ---------- PAGE ROUTES ----------

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/login')
    def login_page():
        return render_template('login.html')

    @app.route('/register')
    def register_page():
        return render_template('register.html')

    @app.route('/dashboard')
    def dashboard():
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        user = User.query.get(session['user_id'])
        notices = Notice.query.order_by(Notice.created.desc()).limit(5).all()
        return render_template('dashboard.html', user=user, notices=notices)

    @app.route('/notices')
    def notices_page():
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        notices = Notice.query.order_by(Notice.created.desc()).all()
        return render_template('notices.html', notices=notices)

    @app.route('/groups')
    def groups_page():
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        groups = StudyGroup.query.all()
        return render_template('groups.html', groups=groups)

    @app.route('/security')
    def security_page():
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        logs = LoginAttempt.query.order_by(LoginAttempt.timestamp.desc()).limit(50).all()
        return render_template('security.html', logs=logs)

    @app.route('/ai')
    def ai_page():
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return render_template('ai.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('home'))

    # ---------- AUTH API ----------

    @app.route('/api/register', methods=['POST'])
    def api_register():
        data = request.form
        if User.query.filter_by(email=data['email']).first():
            return render_template('register.html', error='Email already registered!')
        hashed = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(name=data['name'], email=data['email'], password=hashed)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login_page'))

    @app.route('/api/login', methods=['POST'])
    def api_login():
        data = request.form
        ip = request.remote_addr
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            session['user_id'] = user.id
            session['user_name'] = user.name
            log = LoginAttempt(email=data['email'], ip_address=ip, success=True)
            db.session.add(log)
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            log = LoginAttempt(email=data['email'], ip_address=ip, success=False)
            db.session.add(log)
            db.session.commit()
            return render_template('login.html', error='Invalid email or password!')

    # ---------- NOTICES API ----------

    @app.route('/api/notices', methods=['POST'])
    def add_notice():
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        data = request.form
        notice = Notice(title=data['title'], content=data['content'])
        db.session.add(notice)
        db.session.commit()
        return redirect(url_for('notices_page'))

    # ---------- GROUPS API ----------

    @app.route('/api/groups', methods=['POST'])
    def add_group():
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        data = request.form
        group = StudyGroup(name=data['name'], subject=data['subject'], creator_id=session['user_id'])
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('groups_page'))
    
    @app.route('/api/ask', methods=['POST'])
    def api_ask():
        data = request.get_json()
        question = data.get('question', '')
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        result = ask_ai(question)
        return jsonify(result)