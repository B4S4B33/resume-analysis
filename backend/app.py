"""
Resume Checker Flask API
Provides endpoints for resume analysis and job matching
"""
import os
import pickle
import json
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tempfile
from utils.file_parser import parse_file
from utils.evaluation import evaluate_resume

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'resume_uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Load trained models
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
try:
    with open(os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl'), 'rb') as f:
        tfidf_vectorizer = pickle.load(f)
    with open(os.path.join(MODEL_DIR, 'svm_model.pkl'), 'rb') as f:
        svm_model = pickle.load(f)
    print("Models loaded successfully!")
except Exception as e:
    print(f"Warning: Could not load pre-trained models: {str(e)}")
    print("This is fine for development. Train the model first using the Jupyter notebook.")
    tfidf_vectorizer = None
    svm_model = None


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Resume Checker API',
        'version': '1.0.0'
    }), 200


@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    """
    Analyze resume text or file against job description text or file
    Accepts both text input and file uploads
    """
    try:
        resume_text = None
        job_description = None
        
        # Parse Resume - can be text or file
        if 'resume_file' in request.files:
            file = request.files['resume_file']
            
            if file.filename == '':
                return jsonify({'error': 'No resume file selected'}), 400
            
            if not allowed_file(file.filename):
                return jsonify({
                    'error': f'Resume file type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
                }), 400
            
            # Save and parse resume file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                resume_text = parse_file(filepath)
            finally:
                # Clean up uploaded file
                if os.path.exists(filepath):
                    os.remove(filepath)
        else:
            # Use resume text input
            resume_text = request.form.get('resume_text', '')
        
        if not resume_text:
            return jsonify({'error': 'No resume content provided'}), 400
        
        # Parse Job Description - can be text or file
        if 'job_file' in request.files:
            file = request.files['job_file']
            
            if file.filename == '':
                return jsonify({'error': 'No job description file selected'}), 400
            
            if not allowed_file(file.filename):
                return jsonify({
                    'error': f'Job file type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
                }), 400
            
            # Save and parse job file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                job_description = parse_file(filepath)
            finally:
                # Clean up uploaded file
                if os.path.exists(filepath):
                    os.remove(filepath)
        else:
            # Use job description text input
            job_description = request.form.get('job_description', '')
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        # Perform comprehensive analysis
        analysis_result = evaluate_resume(resume_text, job_description)
        
        return jsonify({
            'success': True,
            'analysis': analysis_result
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Error processing resume: {str(e)}'
        }), 500


@app.route('/api/match', methods=['POST'])
def match_resume_job():
    """
    Match resume against job description
    Uses cosine similarity
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is empty'}), 400
        
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        
        if not resume_text or not job_description:
            return jsonify({
                'error': 'Both resume_text and job_description are required'
            }), 400
        
        # Perform analysis
        analysis_result = evaluate_resume(resume_text, job_description)
        
        return jsonify({
            'success': True,
            'match_score': analysis_result.get('overall_score', 0),
            'keyword_match': analysis_result.get('keyword_match', {}),
            'skills_gap': analysis_result.get('skills_gap', {}),
            'ats_compatibility': analysis_result.get('ats_compatibility', {})
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Error matching resume: {str(e)}'
        }), 500


@app.route('/api/file-upload', methods=['POST'])
def upload_and_parse():
    """
    Upload a resume file and extract text
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Save and parse file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            text_content = parse_file(filepath)
            return jsonify({
                'success': True,
                'filename': filename,
                'content': text_content
            }), 200
        finally:
            # Clean up
            if os.path.exists(filepath):
                os.remove(filepath)
                
    except Exception as e:
        return jsonify({
            'error': f'Error processing file: {str(e)}'
        }), 500


@app.route('/api/classify', methods=['POST'])
def classify_resume():
    """
    Classify resume using trained SVM model
    """
    try:
        if svm_model is None or tfidf_vectorizer is None:
            return jsonify({
                'error': 'Models not loaded. Please train the model first.'
            }), 503
        
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        
        if not resume_text:
            return jsonify({'error': 'resume_text is required'}), 400
        
        # Preprocess and vectorize
        from utils.text_processor import clean_text
        resume_clean = clean_text(resume_text)
        X_vec = tfidf_vectorizer.transform([resume_clean])
        
        # Make prediction
        prediction = svm_model.predict(X_vec)[0]
        probabilities = svm_model.predict_proba(X_vec)[0]
        classes = svm_model.classes_
        
        # Get confidence
        confidence = float(max(probabilities)) * 100
        
        return jsonify({
            'success': True,
            'predicted_category': prediction,
            'confidence': round(confidence, 2),
            'probabilities': {
                str(cls): round(float(prob) * 100, 2) 
                for cls, prob in zip(classes, probabilities)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Error classifying resume: {str(e)}'
        }), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({
        'error': f'File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024):.1f}MB'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("=" * 50)
    print("Resume Checker API Starting...")
    print("=" * 50)
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Allowed file types: {', '.join(ALLOWED_EXTENSIONS)}")
    print(f"Max file size: {MAX_FILE_SIZE / (1024*1024):.1f}MB")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
