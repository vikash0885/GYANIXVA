from flask import Blueprint, render_template, request, jsonify, abort
from flask_login import login_required, current_user
from app.models import ChatSession, ChatMessage
from app.extensions import db
from app.utils.ai_helper import generate_response

chat = Blueprint('chat', __name__)

@chat.route('/chat')
@login_required
def index():
    # Get user's chat history sorted by date
    recent_chats = ChatSession.query.filter_by(user_id=current_user.id).order_by(ChatSession.created_at.desc()).limit(10).all()
    return render_template('chat/index.html', recent_chats=recent_chats, active_session=None)

@chat.route('/chat/<int:session_id>')
@login_required
def session(session_id):
    chat_session = ChatSession.query.get_or_404(session_id)
    if chat_session.user_id != current_user.id:
        abort(403)
        
    recent_chats = ChatSession.query.filter_by(user_id=current_user.id).order_by(ChatSession.created_at.desc()).limit(10).all()
    return render_template('chat/index.html', recent_chats=recent_chats, active_session=chat_session)

@chat.route('/api/chat/send', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()
    message_content = data.get('message')
    session_id = data.get('session_id')
    
    if not message_content:
        return jsonify({'error': 'Message is required'}), 400
        
    # Get or Create Session
    if session_id:
        chat_session = ChatSession.query.get(session_id)
        if not chat_session or chat_session.user_id != current_user.id:
            return jsonify({'error': 'Invalid session'}), 403
    else:
        # Create title from first few words
        title = ' '.join(message_content.split()[:5]) + '...'
        chat_session = ChatSession(user_id=current_user.id, title=title)
        db.session.add(chat_session)
        db.session.commit()
    
    # Save User Message
    user_msg = ChatMessage(session_id=chat_session.id, role='user', content=message_content)
    db.session.add(user_msg)
    
    # Get AI Response
    ai_response_content = generate_response(message_content)
    
    # Save AI Message
    ai_msg = ChatMessage(session_id=chat_session.id, role='ai', content=ai_response_content)
    db.session.add(ai_msg)
    
    db.session.commit()
    
    return jsonify({
        'session_id': chat_session.id,
        'user_message': {'role': 'user', 'content': message_content},
        'ai_message': {'role': 'ai', 'content': ai_response_content}
    })

@chat.route('/chat/delete/<int:session_id>', methods=['POST'])
@login_required
def delete_session(session_id):
    chat_session = ChatSession.query.get_or_404(session_id)
    if chat_session.user_id != current_user.id:
        abort(403)
    
    db.session.delete(chat_session)
    db.session.commit()
    
    return jsonify({'success': True})
