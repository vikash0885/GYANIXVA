from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models import StudyLog
from app.extensions import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.bio = request.form.get('bio')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
        
    return render_template('profile.html', user=current_user)

@main.route('/track-study', methods=['POST'])
@login_required
def track_study():
    data = request.get_json()
    duration = data.get('duration') # in minutes
    if duration:
        log = StudyLog(user_id=current_user.id, duration_minutes=duration, subject="General Study")
        db.session.add(log)
        db.session.commit()
    return jsonify({'success': True})
