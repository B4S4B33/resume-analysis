# Resume Checker - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Browser                          │
│                  (localhost:3000)                        │
└─────────────────────────────────────────────────────────┘
                           │
                           │ HTTP/AXIOS
                           ↓
┌─────────────────────────────────────────────────────────┐
│            Next.js Frontend Application                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Pages:                                           │   │
│  │ - index.js (Main app)                           │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Components:                                      │   │
│  │ - FileUploader (drag-drop upload)              │   │
│  │ - ResultsDisplay (metrics visualization)       │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Services:                                        │   │
│  │ - API Client (lib/api.js)                       │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                           │
                           │ REST API
                           │ (JSON)
                           ↓
┌─────────────────────────────────────────────────────────┐
│        Flask REST API Backend (localhost:5000)          │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Endpoints:                                       │   │
│  │ - GET  /health                                  │   │
│  │ - POST /api/analyze    (main analysis)          │   │
│  │ - POST /api/match      (resume-job matching)    │   │
│  │ - POST /api/classify   (SVM classification)     │   │
│  │ - POST /api/file-upload (document parsing)      │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Processing Modules:                             │   │
│  │ - utils/file_parser.py                          │   │
│  │ - utils/text_processor.py                       │   │
│  │ - utils/evaluation.py                           │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ ML Models:                                       │   │
│  │ - SVM Classifier (svm_model.pkl)               │   │
│  │ - TF-IDF Vectorizer (tfidf_vectorizer.pkl)     │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                           │
                           │ File I/O
                           ↓
┌─────────────────────────────────────────────────────────┐
│        File System & Models                             │
│  ┌─────────────────────────────────────────────────┐   │
│  │ models/                                          │   │
│  │ ├── svm_model.pkl                               │   │
│  │ └── tfidf_vectorizer.pkl                        │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Text Analysis Flow
```
User Input (Resume + Job Description)
    ↓
Frontend Validation
    ↓
API Request (POST /api/analyze)
    ↓
Text Preprocessing (NLTK)
    ↓
Feature Extraction (TF-IDF)
    ↓
Analysis Module
    ├── Grammar/Readability (textstat)
    ├── Keyword Matching (Cosine Similarity)
    ├── ATS Scoring (heuristics)
    └── Skills Gap (keyword extraction)
    ↓
JSON Response
    ↓
Frontend Display
```

### 2. File Upload Flow
```
User Selects File
    ↓
Frontend Validation (type, size)
    ↓
API Request (POST /api/analyze with FormData)
    ↓
File Parsing (PyPDF2/python-docx)
    ↓
Text Extraction
    ↓
Same as Text Flow
```

## Component Interactions

### Frontend Components

```
┌──────────────────────────┐
│      pages/index.js      │
│   (Main Application)     │
└──────────────┬───────────┘
               │
       ┌───────┴────────┐
       │                │
       ↓                ↓
┌────────────────────┐  ┌──────────────────┐
│  FileUploader      │  │  ResultsDisplay  │
│  - Drag & drop     │  │  - Metrics       │
│  - File validation │  │  - Charts        │
└────────────────────┘  │  - Recommendations
├─ state:              └──────────────────┘
│  - fileName
│  - error
└─ handlers:
   - onFileSelect()
   - onDrop()

┌──────────────────────────┐
│    lib/api.js            │
│  (API Client)            │
├─ healthCheck()           │
├─ analyzeResume()         │
├─ matchResume()           │
├─ uploadFile()            │
└─ classifyResume()        │
```

### Backend Modules

```
┌──────────────────┐
│    app.py        │
│  (Flask App)     │
├─ Route handlers  │
└─ Error handling  │
       │
       ├─────────────────────────┐
       │                         │
       ↓                         ↓
┌────────────────────┐    ┌──────────────────┐
│ file_parser.py     │    │ text_processor.py│
├─ parse_txt()      │    ├─ clean_text()    │
├─ parse_pdf()      │    ├─ extract_keywords│
├─ parse_docx()     │    ├─ TF-IDF          │
└─ parse_file()     │    ├─ Cosine Sim      │
                    │    └─ Flesch Score    │
                    │            │
                    │    ┌────────┴─────────┐
                    │    │                  │
                    └────┴─ evaluation.py───┘
                       └─ evaluate_resume()
                          - grammar_readability
                          - keyword_match
                          - ats_compatibility
                          - skills_gap
```

## Technology Stack

### Frontend
- **Framework**: Next.js 13+ (React 18)
- **HTTP Client**: Axios
- **File Handling**: react-dropzone
- **Styling**: CSS3
- **Build Tool**: Webpack (via Next.js)

### Backend
- **Framework**: Flask 2.3+
- **NLP**: NLTK, scikit-learn
- **Text Analysis**: textstat
- **Document Parsing**: PyPDF2, python-docx
- **ML**: SVM (scikit-learn)
- **Vectorization**: TF-IDF

### ML Models
- **Algorithm**: Support Vector Machine (SVM)
- **Feature Extraction**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Similarity**: Cosine Similarity
- **Training**: scikit-learn

## Security Considerations

1. **File Upload**
   - Validate file type and size
   - Use secure filename handling
   - Delete files after processing

2. **API**
   - CORS headers properly configured
   - Input validation on all endpoints
   - Error messages don't leak sensitive info

3. **Data Privacy**
   - No data stored on server
   - Files processed in-memory
   - Temporary uploads cleaned up

## Scalability Options

1. **Horizontal Scaling**
   - Deploy multiple backend instances
   - Use load balancer (Nginx/HAProxy)
   - Share model files or use model server

2. **Caching**
   - Cache analysis results
   - Cache vectorizer transformations
   - Implement Redis for session data

3. **Async Processing**
   - Use Celery for long-running tasks
   - Queue for file processing
   - WebSocket for real-time updates

4. **Database**
   - Store analysis history
   - User preferences
   - Model performance metrics

## Performance Optimization

1. **Code Level**
   - Lazy load models
   - Batch processing for multiple resumes
   - Optimize vectorizer (limit features)

2. **Network**
   - Gzip compression
   - CDN for static assets
   - HTTP/2 support

3. **Frontend**
   - Code splitting
   - Image optimization
   - Lazy load components

4. **Backend**
   - Use Gunicorn (multiple workers)
   - Database connection pooling
   - Caching headers
