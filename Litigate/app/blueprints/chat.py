from flask import Blueprint, request, jsonify, session,url_for,redirect,flash
from functools import wraps
from datetime import datetime
from ..extensions import db  # Make sure to import your database instance
from ..database.models import ChatSession, Conversation  # Import your models
from werkzeug.security import check_password_hash, generate_password_hash
from ..nlp.nlp_engine import get_response  # Import your AI response function
# Creating the chat Blueprint
chat = Blueprint('chat', __name__)
responses = []
interactions = []

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to be logged in to view this page.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@chat.route('/start_chat_session', methods=['POST','GET'])
@login_required
def start_chat_session():
    
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    new_chat_session = ChatSession(user_id=user_id, start_time=datetime.utcnow())
    db.session.add(new_chat_session)
    db.session.commit()

    # Set the chat_session_id in the user's session
    session['chat_session_id'] = new_chat_session.id

    return jsonify({'message': 'New chat session created', 'session_id': new_chat_session.id}), 201

@chat.route('/get_chat_sessions', methods=['GET'])
@login_required
def get_chat_sessions():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    chat_sessions = ChatSession.query.filter_by(user_id=user_id).all()
    sessions_json = [{'id': session.id, 'start_time': session.start_time.strftime("%Y-%m-%d %H:%M:%S")} for session in chat_sessions]

    return jsonify(sessions_json)

@chat.route('/get_conversations/<int:session_id>', methods=['GET'])
@login_required
def get_conversations(session_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    chat_session = ChatSession.query.filter_by(id=session_id, user_id=user_id).first()
    if not chat_session:
        return jsonify({'error': 'Chat session not found or access denied'}), 404

    conversations = Conversation.query.filter_by(chat_session_id=session_id).order_by(Conversation.timestamp.asc()).all()

    conversation_data = [{
        'type': conv.type,  # Use the 'type' directly from the model
        'message': conv.message
    } for conv in conversations]

    return jsonify(conversation_data)

@chat.route('/save_interaction', methods=['POST'])
@login_required
def save_interaction():
    data = request.json
    user_id = session.get('user_id')
    # Retrieve the current chat session ID from the session or other means
    chat_session_id = session.get('chat_session_id')  # Ensure this is being set somewhere in your application

    user_input = data['user_input']
    ai_response = data['ai_response']

    # Save both messages with their respective types
    save_conversation_message(user_id, chat_session_id, user_input, 'user')
    save_conversation_message(user_id, chat_session_id, ai_response, 'ai')

    return jsonify({'status': 'success'})

def save_conversation_message(user_id, chat_session_id, message, message_type):
    # Create a new message with the chat session ID
    new_message = Conversation(chat_session_id=chat_session_id, message=message, type=message_type)
    db.session.add(new_message)
    db.session.commit()

@chat.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    user_id = session.get('user_id')
    interactions = []  # Adjust as needed

    if request.method == 'POST':
        print("this works")
        if request.is_json:
            data = request.get_json()
            user_input = data.get('user_input')
        else:
            user_input = request.form.get('user_input')
        print(user_input)
        if not user_input:
            return jsonify({'error': 'No user input provided'}), 400

        # Example process, adjust as needed
        ai_response = get_response(user_input)
        
        interactions.append({'type': 'user', 'text': user_input})
        interactions.append({'type': 'ai', 'text': ai_response})
        print(ai_response)
        return jsonify({'user_input': user_input, 'ai_response': ai_response})
    
@chat.route('/end_chat_session', methods=['POST','GET'])
@login_required
def end_chat_session():
    if 'chat_session_id' in session:
        chat_session_id = session['chat_session_id']
        # Here you can update the database to mark the chat session as ended, if needed
        session.pop('chat_session_id', None)  # Remove chat_session_id from session
        return redirect(url_for('chat.start_chat_session')),200
    return jsonify({'error': 'No active chat session'}), 400


@chat.route('/fetch_chat_histories')
@login_required
def fetch_chat_histories():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    chat_sessions = ChatSession.query.filter_by(user_id=user_id).all()

    chat_histories = []
    for chat_session in chat_sessions:
        # Fetch the first user and AI messages in this session as a snippet
        user_message = Conversation.query.filter_by(chat_session_id=chat_session.id, type='user').first()
        ai_message = Conversation.query.filter_by(chat_session_id=chat_session.id, type='ai').first()

        chat_histories.append({
            'session_id': chat_session.id,
            'user_snippet': user_message.message if user_message else 'No message',
            'ai_snippet': ai_message.message if ai_message else 'No response'
        })

    return jsonify(chat_histories)
