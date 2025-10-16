"""
GenAI Creator - Flask Backend
A web application for generating AI content (art, music, code, text)
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import os
import json
import requests
from datetime import datetime
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Configuration
DATABASE = 'genai_creator.db'
UPLOAD_FOLDER = 'static/generated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# API Keys - Store these in environment variables for production
API_KEYS = {
    'openai': os.environ.get('OPENAI_API_KEY', 'your-openai-api-key'),
    'stability': os.environ.get('STABILITY_API_KEY', 'your-stability-api-key'),
}

# Database initialization
def init_db():
    """Initialize SQLite database with required schema"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            content_type TEXT NOT NULL,
            result TEXT NOT NULL,
            file_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def save_to_database(prompt, content_type, result, file_path=None):
    """Save generation data to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO generations (prompt, content_type, result, file_path)
        VALUES (?, ?, ?, ?)
    ''', (prompt, content_type, result, file_path))
    
    conn.commit()
    generation_id = cursor.lastrowid
    conn.close()
    
    return generation_id

# AI Generation Functions

def generate_art(prompt):
    """Generate art using Stability AI or DALL-E API"""
    try:
        # Using OpenAI DALL-E API
        headers = {
            'Authorization': f'Bearer {API_KEYS["openai"]}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'dall-e-3',
            'prompt': prompt,
            'n': 1,
            'size': '1024x1024'
        }
        
        response = requests.post(
            'https://api.openai.com/v1/images/generations',
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            image_url = result['data'][0]['url']
            
            # Download and save image locally
            img_response = requests.get(image_url)
            filename = f"art_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            with open(filepath, 'wb') as f:
                f.write(img_response.content)
            
            return {
                'success': True,
                'result': image_url,
                'file_path': filepath,
                'local_url': f'/static/generated/{filename}'
            }
        else:
            return {
                'success': False,
                'result': f'API Error: {response.status_code} - {response.text}'
            }
            
    except Exception as e:
        return {
            'success': False,
            'result': f'Error generating art: {str(e)}'
        }

def generate_music(prompt):
    """Generate music description or audio (placeholder for music API)"""
    try:
        # Note: Most music generation APIs require special access
        # This is a placeholder implementation
        # You can integrate with APIs like: Mubert, AIVA, or OpenAI Audio
        
        result_text = f"Music Generation Placeholder:\n\nPrompt: {prompt}\n\n"
        result_text += "Note: To generate actual music, integrate with:\n"
        result_text += "- Mubert API (https://mubert.com/)\n"
        result_text += "- AIVA API (https://www.aiva.ai/)\n"
        result_text += "- Suno AI (https://suno.ai/)\n\n"
        result_text += "For now, this is a text description of the requested music."
        
        return {
            'success': True,
            'result': result_text,
            'file_path': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'result': f'Error generating music: {str(e)}'
        }

def generate_code(prompt):
    """Generate code using OpenAI API"""
    try:
        headers = {
            'Authorization': f'Bearer {API_KEYS["openai"]}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-4',
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are an expert programmer. Generate clean, well-commented, functional code.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': 0.7,
            'max_tokens': 2000
        }
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            code = result['choices'][0]['message']['content']
            
            return {
                'success': True,
                'result': code,
                'file_path': None
            }
        else:
            return {
                'success': False,
                'result': f'API Error: {response.status_code} - {response.text}'
            }
            
    except Exception as e:
        return {
            'success': False,
            'result': f'Error generating code: {str(e)}'
        }

def generate_content(prompt):
    """Generate text content using OpenAI API"""
    try:
        headers = {
            'Authorization': f'Bearer {API_KEYS["openai"]}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-4',
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a creative content writer. Generate engaging, well-structured content.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': 0.8,
            'max_tokens': 1500
        }
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            return {
                'success': True,
                'result': content,
                'file_path': None
            }
        else:
            return {
                'success': False,
                'result': f'API Error: {response.status_code} - {response.text}'
            }
            
    except Exception as e:
        return {
            'success': False,
            'result': f'Error generating content: {str(e)}'
        }

# Routes

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """
    Handle content generation requests
    Expected JSON: { "prompt": "...", "type": "art|music|code|content" }
    """
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        content_type = data.get('type', '').lower()
        
        # Validation
        if not prompt:
            return jsonify({
                'success': False,
                'result': 'Prompt is required'
            }), 400
        
        if content_type not in ['art', 'music', 'code', 'content']:
            return jsonify({
                'success': False,
                'result': 'Invalid content type'
            }), 400
        
        # Generate content based on type
        if content_type == 'art':
            result = generate_art(prompt)
        elif content_type == 'music':
            result = generate_music(prompt)
        elif content_type == 'code':
            result = generate_code(prompt)
        elif content_type == 'content':
            result = generate_content(prompt)
        
        # Save to database
        if result['success']:
            save_to_database(
                prompt=prompt,
                content_type=content_type,
                result=result['result'],
                file_path=result.get('file_path')
            )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'result': f'Server error: {str(e)}'
        }), 500

@app.route('/history', methods=['GET'])
def history():
    """
    Get generation history
    Returns all past prompts and results
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, prompt, content_type, result, file_path, created_at
            FROM generations
            ORDER BY created_at DESC
            LIMIT 50
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        history_data = []
        for row in rows:
            history_data.append({
                'id': row['id'],
                'prompt': row['prompt'],
                'content_type': row['content_type'],
                'result': row['result'],
                'file_path': row['file_path'],
                'created_at': row['created_at']
            })
        
        return jsonify({
            'success': True,
            'history': history_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'result': f'Error fetching history: {str(e)}'
        }), 500

@app.route('/download/<int:generation_id>')
def download(generation_id):
    """Download generated file"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT file_path, content_type FROM generations WHERE id = ?
        ''', (generation_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row and row['file_path'] and os.path.exists(row['file_path']):
            return send_file(row['file_path'], as_attachment=True)
        else:
            return jsonify({
                'success': False,
                'result': 'File not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'result': f'Error downloading file: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)