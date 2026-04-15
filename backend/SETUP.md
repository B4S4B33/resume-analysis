# Backend Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip or conda package manager
- Virtual environment (recommended)

## Installation Steps

### 1. Create and Activate Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download NLTK Data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 4. Train the Model

Open Jupyter and run the training notebook:
```bash
jupyter notebook notebooks/train_model.ipynb
```

Or using Jupyter Lab:
```bash
jupyter lab notebooks/train_model.ipynb
```

**Follow the cells in order:**
1. Import libraries
2. Load resume dataset
3. Preprocess text
4. Extract TF-IDF features
5. Train SVM model
6. Save models to `models/` folder

### 5. Start Flask API
```bash
python app.py
```

The API will be available at: `http://localhost:5000`

## API Testing

### Health Check
```bash
curl http://localhost:5000/health
```

### Analyze Resume
```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "resume_text=Your resume text here" \
  -F "job_description=Job description here"
```

### Match Resume (JSON)
```bash
curl -X POST http://localhost:5000/api/match \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Your resume text",
    "job_description": "Job description"
  }'
```

## Troubleshooting

- **ModuleNotFoundError**: Run `pip install -r requirements.txt` again
- **NLTK data not found**: Run the download command
- **Port 5000 already in use**: Change port in `app.py` line
- **Models not found**: Run training notebook first

## File Structure
```
backend/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── models/
│   ├── svm_model.pkl
│   └── tfidf_vectorizer.pkl
├── notebooks/
│   └── train_model.ipynb
└── utils/
    ├── file_parser.py
    ├── text_processor.py
    └── evaluation.py
```
