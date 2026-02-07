import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.utils.ai_helper import analyze_image, generate_notes

ai_features = Blueprint('ai', __name__)

@ai_features.route('/ai/notes', methods=['GET', 'POST'])
@login_required
def notes():
    result = None
    topic = None
    if request.method == 'POST':
        topic = request.form.get('topic')
        note_type = request.form.get('type')
        if topic:
            result = generate_notes(topic, note_type)
    return render_template('ai/notes.html', result=result, topic=topic)

@ai_features.route('/ai/image-solver', methods=['GET', 'POST'])
@login_required
def image_solver():
    solution = None
    image_url = None
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
            
        if file:
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            
            # Ensure folder exists
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            
            file.save(upload_path)
            image_url = url_for('static', filename='uploads/' + filename)
            
            solution = analyze_image(filename)
            
    return render_template('ai/image_solver.html', solution=solution, image_url=image_url)

@ai_features.route('/ai/tutor')
@login_required
def tutor():
    # Mock Data
    weak_areas = ['Thermodynamics', 'Calculus Integration', 'Modern History']
    suggestions = [
        'Review Chapter 4 of Physics.',
        'Practice 10 problems on Integration.',
        'Watch a documentary on World War II.'
    ]
    return render_template('ai/tutor.html', weak_areas=weak_areas, suggestions=suggestions)
