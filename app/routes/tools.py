from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user
from datetime import datetime, date
from app.models import StudyPlan
from app.extensions import db
from app.utils.ai_helper import generate_response
import json

tools = Blueprint('tools', __name__)

@tools.route('/tools/planner', methods=['GET', 'POST'])
@login_required
def planner():
    if request.method == 'POST':
        goal = request.form.get('goal')
        subjects = request.form.get('subjects')
        hours = request.form.get('hours')
        target_date_str = request.form.get('target_date')
        
        target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date() if target_date_str else None
        
        # AI Prompt engineering (simplified)
        prompt = f"Create a study plan for {goal}. Subjects: {subjects}. Available: {hours} hours/day. Deadline: {target_date_str}. Format as HTML compatible list."
        plan_content = generate_response(prompt)
        
        new_plan = StudyPlan(
            user_id=current_user.id,
            goal=goal,
            subjects=subjects,
            daily_hours=float(hours) if hours else 0,
            target_date=target_date,
            content=plan_content
        )
        
        db.session.add(new_plan)
        db.session.commit()
        
        flash('Study Plan Generated!', 'success')
        return redirect(url_for('tools.view_plan', plan_id=new_plan.id))
        
    return render_template('tools/planner_form.html')

@tools.route('/tools/planner/<int:plan_id>')
@login_required
def view_plan(plan_id):
    plan = StudyPlan.query.get_or_404(plan_id)
    if plan.user_id != current_user.id:
        abort(403)
    return render_template('tools/planner_view.html', plan=plan)

@tools.route('/tools/solver', methods=['GET', 'POST'])
@login_required
def solver():
    solution = None
    question = None
    if request.method == 'POST':
        question = request.form.get('question')
        if question:
            solution = generate_response(f"Solve this Question step-by-step: {question}")
            
    return render_template('tools/solver.html', question=question, solution=solution)
