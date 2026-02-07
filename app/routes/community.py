from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import StudyGroup, GroupMessage
from app.extensions import db

community = Blueprint('community', __name__)

@community.route('/community/groups', methods=['GET', 'POST'])
@login_required
def groups():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if name:
            new_group = StudyGroup(name=name, description=description)
            db.session.add(new_group)
            db.session.commit()
            flash('Group created!', 'success')
            return redirect(url_for('community.groups'))
            
    all_groups = StudyGroup.query.all()
    # Seed default groups if empty
    if not all_groups:
        db.session.add(StudyGroup(name="JEE Aspirants 2026", description="Discuss Physics, Chem, Maths."))
        db.session.add(StudyGroup(name="UPSC Warriors", description="Daily current affairs discussion."))
        db.session.commit()
        all_groups = StudyGroup.query.all()
        
    return render_template('community/index.html', groups=all_groups)

@community.route('/community/groups/<int:group_id>', methods=['GET', 'POST'])
@login_required
def group_chat(group_id):
    group = StudyGroup.query.get_or_404(group_id)
    
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            msg = GroupMessage(content=content, user_id=current_user.id, group_id=group.id)
            db.session.add(msg)
            db.session.commit()
            
    return render_template('community/group.html', group=group)
