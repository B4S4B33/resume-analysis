# Resume Checker - API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication
No authentication required (open API for local development)

---

## Endpoints

### 1. Health Check

**Endpoint**: `GET /health`

**Description**: Check if the API is running and healthy

**Request**:
```bash
curl -X GET http://localhost:5000/health
```

**Response** (200):
```json
{
  "status": "healthy",
  "service": "Resume Checker API",
  "version": "1.0.0"
}
```

---

### 2. Analyze Resume

**Endpoint**: `POST /api/analyze`

**Description**: Analyze a resume against a job description (supports text or file input)

**Request - Text Input**:
```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "resume_text=Python developer with 5 years experience" \
  -F "job_description=We need a senior Python developer with Django experience"
```

**Request - File Input**:
```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "resume_file=@resume.pdf" \
  -F "job_description=Senior Python developer needed"
```

**Parameters**:
- `resume_text` (string): Resume content as text
- `resume_file` (file): Resume file (.txt, .pdf, .docx)
- `job_description` (string, required): Job description text

**Response** (200):
```json
{
  "success": true,
  "analysis": {
    "grammar_readability": {
      "word_count": 450,
      "flesch_score": 52.3,
      "readability_level": "Standard"
    },
    "keyword_match": {
      "score": 72.5,
      "matched_keywords": ["python", "django", "rest api"],
      "missing_keywords": ["kubernetes", "docker"],
      "match_percentage": 60.0
    },
    "ats_compatibility": {
      "score": 78.5,
      "level": "Good"
    },
    "skills_gap": {
      "found_skills": ["python", "flask"],
      "missing_skills": ["kubernetes"],
      "all_detected_skills": ["python", "flask", "sql"],
      "gap_percentage": 33.33
    },
    "overall_score": 74.5,
    "recommendations": [
      "Incorporate more job-specific keywords: kubernetes, docker, aws",
      "Your resume looks great!"
    ]
  }
}
```

**Error Response** (400):
```json
{
  "error": "Job description is required"
}
```

**Error Response** (500):
```json
{
  "error": "Error processing resume: [details]"
}
```

---

### 3. Match Resume Against Job

**Endpoint**: `POST /api/match`

**Description**: Match resume against job description using cosine similarity

**Request**:
```bash
curl -X POST http://localhost:5000/api/match \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Python Django Flask REST API developer",
    "job_description": "Senior Python developer with Django experience"
  }'
```

**Parameters (JSON)**:
- `resume_text` (string, required): Resume content
- `job_description` (string, required): Job description

**Response** (200):
```json
{
  "success": true,
  "match_score": 72.5,
  "keyword_match": {
    "score": 72.5,
    "matched_keywords": ["python", "django"],
    "missing_keywords": ["aws", "kubernetes"],
    "match_percentage": 50.0
  },
  "skills_gap": {
    "found_skills": ["python", "flask"],
    "missing_skills": ["aws"],
    "all_detected_skills": ["python", "flask"],
    "gap_percentage": 50.0
  },
  "ats_compatibility": {
    "score": 78.5,
    "level": "Good"
  }
}
```

---

### 4. Upload and Parse File

**Endpoint**: `POST /api/file-upload`

**Description**: Upload a resume file and extract text content (without analysis)

**Request**:
```bash
curl -X POST http://localhost:5000/api/file-upload \
  -F "file=@resume.pdf"
```

**Parameters**:
- `file` (file, required): Document file (.txt, .pdf, .docx)

**Response** (200):
```json
{
  "success": true,
  "filename": "resume.pdf",
  "content": "Senior Software Engineer with 7 years experience..."
}
```

**Error Response** (400):
```json
{
  "error": "File type not allowed. Allowed types: txt, pdf, docx"
}
```

**Error Response** (413):
```json
{
  "error": "File too large. Maximum size: 10.0MB"
}
```

---

### 5. Classify Resume

**Endpoint**: `POST /api/classify`

**Description**: Classify resume into job categories using trained SVM model

**Request**:
```bash
curl -X POST http://localhost:5000/api/classify \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Senior Software Engineer with Python expertise"
  }'
```

**Parameters (JSON)**:
- `resume_text` (string, required): Resume content

**Response** (200):
```json
{
  "success": true,
  "predicted_category": "Software Engineer",
  "confidence": 85.3,
  "probabilities": {
    "Software Engineer": 85.3,
    "Data Scientist": 10.2,
    "DevOps Engineer": 4.5
  }
}
```

**Error Response** (503):
```json
{
  "error": "Models not loaded. Please train the model first."
}
```

---

## Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | Success | Request processed successfully |
| 400 | Bad Request | Check required parameters |
| 413 | Payload Too Large | Reduce file size (max 10MB) |
| 500 | Server Error | Check server logs |
| 503 | Service Unavailable | Train ML models first |

---

## File Upload Limits

- **Max File Size**: 10 MB
- **Allowed Formats**: 
  - `.txt` (Plain text)
  - `.pdf` (PDF documents)
  - `.docx` (Word documents)

---

## CORS Headers

All endpoints support CORS. The following headers are available:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

## Example Usage - JavaScript/Axios

```javascript
import axios from 'axios';

const API_URL = 'http://localhost:5000';

// Analyze with text
async function analyzeResume(resumeText, jobDescription) {
  try {
    const formData = new FormData();
    formData.append('resume_text', resumeText);
    formData.append('job_description', jobDescription);
    
    const response = await axios.post(
      `${API_URL}/api/analyze`,
      formData
    );
    
    return response.data;
  } catch (error) {
    console.error('Error:', error.response.data);
  }
}

// Analyze with file
async function analyzeWithFile(file, jobDescription) {
  try {
    const formData = new FormData();
    formData.append('resume_file', file);
    formData.append('job_description', jobDescription);
    
    const response = await axios.post(
      `${API_URL}/api/analyze`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    
    return response.data;
  } catch (error) {
    console.error('Error:', error.response.data);
  }
}

// Match resume
async function matchResume(resumeText, jobDescription) {
  try {
    const response = await axios.post(
      `${API_URL}/api/match`,
      {
        resume_text: resumeText,
        job_description: jobDescription,
      }
    );
    
    return response.data;
  } catch (error) {
    console.error('Error:', error.response.data);
  }
}
```

---

## Example Usage - Python

```python
import requests

API_URL = 'http://localhost:5000'

# Analyze with text
def analyze_resume(resume_text, job_description):
    data = {
        'resume_text': resume_text,
        'job_description': job_description
    }
    response = requests.post(f'{API_URL}/api/analyze', data=data)
    return response.json()

# Analyze with file
def analyze_with_file(file_path, job_description):
    with open(file_path, 'rb') as f:
        files = {'resume_file': f}
        data = {'job_description': job_description}
        response = requests.post(
            f'{API_URL}/api/analyze',
            files=files,
            data=data
        )
    return response.json()

# Match resume
def match_resume(resume_text, job_description):
    data = {
        'resume_text': resume_text,
        'job_description': job_description
    }
    response = requests.post(f'{API_URL}/api/match', json=data)
    return response.json()

# Usage
result = analyze_resume(
    "Python developer with 5 years experience",
    "Senior Python developer needed"
)
print(result)
```

---

## Response Structure

All responses follow this pattern:

**Success**:
```json
{
  "success": true,
  "data": { /* endpoint-specific data */ }
}
```

**Error**:
```json
{
  "error": "Error message describing what went wrong"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider adding:
- Per-IP rate limiting
- Per-user rate limiting
- Request queuing for large files

---

## Performance Tips

1. **Batch Processing**: Process multiple resumes in parallel
2. **Caching**: Cache analysis results for identical inputs
3. **Async**: Use async requests for better performance
4. **Compression**: Enable gzip compression

---

## API Status

Check API status at: `GET /health`

---

## Support

For issues or questions:
1. Check error response messages
2. Review documentation
3. Check server logs
4. Verify ML models are trained

---

**Last Updated**: 2024
**API Version**: 1.0.0
