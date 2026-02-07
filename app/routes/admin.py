from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from app.models import User, StudyGroup, StudyPlan
from functools import wraps

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    stats = {
        'users': User.query.count(),
        'groups': StudyGroup.query.count(),
        'plans': StudyPlan.query.count()
    }
    users = User.query.limit(20).all()
    return render_template('admin/dashboard.html', stats=stats, users=users)
