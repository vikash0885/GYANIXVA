from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.models import College, Exam, NewsItem
from app.extensions import db

resources = Blueprint('resources', __name__)

@resources.route('/resources/colleges')
@login_required
def colleges():
    # Auto-seed if empty
    if College.query.count() == 0:
        seed_data()
        
    location = request.args.get('location')
    course = request.args.get('course')
    
    query = College.query
    
    if location:
        query = query.filter(College.location.ilike(f'%{location}%'))
    if course:
        query = query.filter(College.course.ilike(f'%{course}%'))
        
    colleges_list = query.all()
    
    # AI Fallback if no results found
    is_ai_generated = False
    if not colleges_list and (location or course):
        try:
            from app.utils.ai_helper import generate_response
            import json
            
            prompt = f"""
            List 3 top colleges in {location or 'India'} for {course or 'any course'}. 
            Provide details in valid JSON format:
            [
                {{"name": "College Name", "location": "City", "course": "Course", "fees": "Fees", "ranking": 1, "exams_required": "Exam Name"}}
            ]
            Do not include any text outside the JSON array.
            """
            response = generate_response(prompt)
            # Clean response to ensure valid JSON
            start = response.find('[')
            end = response.rfind(']') + 1
            if start != -1 and end != -1:
                json_data = json.loads(response[start:end])
                for item in json_data:
                    colleges_list.append(College(
                        name=item.get('name', 'Unknown'),
                        location=item.get('location', location),
                        course=item.get('course', course),
                        fees=item.get('fees', 'N/A'),
                        ranking=item.get('ranking', 0),
                        exams_required=item.get('exams_required', 'N/A')
                    ))
                is_ai_generated = True
        except Exception as e:
            print(f"AI Search Error: {e}")
            
    return render_template('resources/college_finder.html', colleges=colleges_list, is_ai_generated=is_ai_generated)

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
        colleges = [
            # Engineering
            College(name="IIT Delhi", location="New Delhi", course="B.Tech", fees="2 Lakhs/Year", ranking=1, exams_required="JEE Advanced"),
            College(name="IIT Bombay", location="Mumbai", course="B.Tech", fees="2.2 Lakhs/Year", ranking=3, exams_required="JEE Advanced"),
            College(name="NIT Trichy", location="Trichy", course="B.Tech", fees="1.5 Lakhs/Year", ranking=8, exams_required="JEE Mains"),
            College(name="BITS Pilani", location="Pilani", course="B.Tech", fees="5 Lakhs/Year", ranking=5, exams_required="BITSAT"),
            
            # Medical
            College(name="AIIMS Delhi", location="New Delhi", course="MBBS", fees="5k/Year", ranking=1, exams_required="NEET"),
            College(name="CMC Vellore", location="Vellore", course="MBBS", fees="60k/Year", ranking=3, exams_required="NEET"),
            
            # Management
            College(name="IIM Ahmedabad", location="Ahmedabad", course="MBA", fees="25 Lakhs/Total", ranking=1, exams_required="CAT"),
            College(name="FMS Delhi", location="New Delhi", course="MBA", fees="2 Lakhs/Total", ranking=4, exams_required="CAT"),
            
            # BCA & Computer Applications
            College(name="Christ University", location="Bangalore", course="BCA", fees="1.5 Lakhs/Year", ranking=1, exams_required="CUET"),
            College(name="Symbiosis Institute of Computer Studies", location="Pune", course="BCA", fees="2 Lakhs/Year", ranking=2, exams_required="SET"),
            College(name="Loyola College", location="Chennai", course="BCA", fees="50k/Year", ranking=3, exams_required="Merit"),
            College(name="Amity University", location="Noida", course="BCA", fees="1.8 Lakhs/Year", ranking=5, exams_required="Direct/Interview"),
            College(name="IP University (GGSIPU)", location="New Delhi", course="BCA", fees="90k/Year", ranking=6, exams_required="IPU CET"),
            
            # Arts & Commerce
            College(name="SRCC", location="New Delhi", course="B.Com Hons", fees="30k/Year", ranking=1, exams_required="CUET"),
            College(name="St. Stephen's College", location="New Delhi", course="BA English", fees="40k/Year", ranking=1, exams_required="CUET"),
            College(name="Hindu College", location="New Delhi", course="BA Pol Science", fees="35k/Year", ranking=2, exams_required="CUET"),
            
            # Law
            College(name="NLSIU Bangalore", location="Bangalore", course="BA LLB", fees="3 Lakhs/Year", ranking=1, exams_required="CLAT"),
            College(name="NLU Delhi", location="New Delhi", course="BA LLB", fees="2.5 Lakhs/Year", ranking=2, exams_required="AILET"),
        ]
        
        for college in colleges:
            db.session.add(college)
    
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
