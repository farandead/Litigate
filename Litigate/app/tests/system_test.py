import pytest
from app import create_app  # Adjust the import as per your application structure
from app.extensions import db as _db
from app.database.models import ChatSession, Conversation,User
from flask import *
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from app.extensions import db
import requests
import openai
# from openai import OpenAI
import os
from app.database.models import *
from datetime import datetime
from app.blueprints.auth import auth
from app.blueprints.chat import chat

        
@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()  
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client

@pytest.fixture(scope='module')
def init_database(test_client):
  
    _db.create_all()

    user1 = User(id=1, username='TestUser', password='Password')
    _db.session.add(user1)
    _db.session.commit()

    yield  # No need to return _db

    _db.session.remove()
    _db.drop_all()

# Adjusted to use the init_database fixture for database setup
def test_start_chat_session_authenticated(test_client, init_database):
    with test_client.session_transaction() as sess:
        sess['user_id'] = 1

    response = test_client.post('/chat/start_chat_session')
    assert response.status_code == 201

def test_start_chat_session_unauthenticated(test_client):
    with test_client.session_transaction() as sess:
        sess.pop('user_id', None)

    response = test_client.post('/chat/start_chat_session')
    assert response.status_code == 302  # Or 401, depending on your auth handling

def test_get_chat_sessions_authenticated(test_client, init_database):
    with test_client.session_transaction() as session:
        session['user_id'] = 1

    response = test_client.get('/chat/get_chat_sessions')
    assert response.status_code == 200

def test_get_chat_sessions_unauthenticated(test_client):
    response = test_client.get('/chat/get_chat_sessions')
    assert response.status_code == 200

# Make sure this test also uses the init_database fixture
def test_save_interaction_authenticated(test_client, init_database):
    # Ensuring a chat session exists in the database for the user
    chat_session = ChatSession(user_id=1, start_time=datetime.utcnow())
    _db.session.add(chat_session)
    _db.session.commit()

    with test_client.session_transaction() as session:
        session['user_id'] = 1
        session['chat_session_id'] = chat_session.id

    data = {'user_input': 'Hello', 'ai_response': 'Hi there!'}
    response = test_client.post('/chat/save_interaction', json=data)
    assert response.status_code == 200
    assert b'success' in response.data

def test_register(test_client, init_database):
    # Mimic form submission with POST data for registration
    response = test_client.post('/auth/register', data={
        'username': 'testuser2',
        'password': 'testpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert User.query.filter_by(username='testuser').first() is not None

def test_login_success(test_client, init_database):
    # First, create a user
    hashed_password = generate_password_hash('mysecurepassword')
    user = User(username='existinguser', password=hashed_password)
    _db.session.add(user)
    _db.session.commit()

    # Attempt to login
    response = test_client.post('/auth/login', data={
        'username': 'existinguser',
        'password': 'mysecurepassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'user_id' in session

def test_login_failure(test_client, init_database):
    # Perform the login POST request directly with test_client
    response = test_client.post('/auth/login', data={
        'username': 'wronguser',
        'password': 'wrongpassword'
    }, follow_redirects=True)

    # Assertions about the response
    assert response.status_code == 200
    assert 'Invalid username or password.' in response.data.decode('utf-8')

from uuid import uuid4

def login_user(test_client, username=None, password="testpassword"):
    if username is None:
        username = f"user_{uuid4()}"  # Generate a unique username
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    with test_client.session_transaction() as session:
        session['user_id'] = user.id  # Mock login
def test_submit(test_client, init_database):
    login_user(test_client)
    user_input = "Hello, AI!"
    response = test_client.post('/chat/submit', data=json.dumps({"user_input": user_input}), content_type='application/json')
    data = response.get_json()
    assert response.status_code == 200
    assert data['user_input'] == user_input
    # Further assert the AI response as needed based on your application's logic

def test_end_chat_session(test_client, init_database):
    login_user(test_client)
    with test_client.session_transaction() as session:
        session['chat_session_id'] = 1  

    response = test_client.get('/chat/end_chat_session', follow_redirects=True)
    assert response.status_code == 200


def test_fetch_chat_histories(test_client, init_database):
    login_user(test_client, "user_for_history", "password")
    user = User.query.filter_by(username="user_for_history").first()

    # Create mock chat sessions and messages
    chat_session = ChatSession(user_id=user.id)
    db.session.add(chat_session)
    db.session.commit()

    message1 = Conversation(chat_session_id=chat_session.id, message="Hi", type='user')
    message2 = Conversation(chat_session_id=chat_session.id, message="Hello", type='ai')
    db.session.add_all([message1, message2])
    db.session.commit()

    response = test_client.get('/chat/fetch_chat_histories')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) > 0  # Assuming at least one history exists
    # Further asserts can check the structure of the returned history data