from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.models import College, Exam, NewsItem
from app.extensions import db

resources = Blueprint('resources', __name__)

@resources.route('/resources/colleges')
@login_required
def colleges():
    query = request.args.get('search')
    if query:
        colleges_list = College.query.filter(College.name.contains(query) | College.course.contains(query)).all()
    else:
        # Limit to 10 for display
        colleges_list = College.query.limit(10).all()
    return render_template('resources/college_finder.html', colleges=colleges_list)

@resources.route('/resources/exams')
@login_required
def exams():
    exams_list = Exam.query.all()
    return render_template('resources/exam_guide.html', exams=exams_list)

@resources.route('/resources/news')
@login_required
def news():
    news_list = NewsItem.query.order_by(NewsItem.created_at.desc()).all()
    return render_template('resources/news_feed.html', news=news_list)

# Admin routes for populating data (simplified for this iteration)
@resources.route('/resources/seed_data')
@login_required
def seed_data():
    # Simple seeder for demo
    if not College.query.first():
        db.session.add(College(name="IIT Delhi", location="New Delhi", course="B.Tech", fees="2 Lakhs/Year", ranking=1, exams_required="JEE Advanced"))
        db.session.add(College(name="AIIMS Delhi", location="New Delhi", course="MBBS", fees="5k/Year", ranking=1, exams_required="NEET"))
        db.session.add(College(name="IIM Ahmedabad", location="Ahmedabad", course="MBA", fees="25 Lakhs/Total", ranking=1, exams_required="CAT"))
    
    if not Exam.query.first():
        db.session.add(Exam(name="JEE Mains", description="Joint Entrance Examination for Engineering", date=None))
        db.session.add(Exam(name="NEET", description="National Eligibility cum Entrance Test for Medical", date=None))
        db.session.add(Exam(name="UPSC CSE", description="Civil Services Examination", date=None))
        
    if not NewsItem.query.first():
        db.session.add(NewsItem(title="JEE Mains Dates Announced", content="The NTA has announced dates for Session 1...", category="Exam Alert"))
        db.session.add(NewsItem(title="Scholarship for Meritorious Students", content="Government launches new scholarship scheme...", category="Scholarship"))

    db.session.commit()
    flash('Demo data seeded!', 'success')
    return redirect(url_for('resources.colleges'))
