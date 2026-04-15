# Resume Checker - AI-Powered Resume Analysis & Job Matching

A comprehensive web application that analyzes resumes and matches them against job descriptions using machine learning, NLP, and readability metrics.

## Features

### 📊 Analysis Metrics
- **Grammar & Readability**: Word count and Flesch Reading Ease Score
- **Keyword Match**: TF-IDF vectorization and Cosine Similarity analysis
- **ATS Compatibility**: Applicant Tracking System friendliness scoring
- **Skills Gap Analysis**: Identifies missing and matched skills
- **Overall Score**: Comprehensive match percentage

### 📁 File Support
- Text files (.txt)
- PDF documents (.pdf)
- Word documents (.docx)

### 🤖 ML Models
- **SVM Classifier**: Resume categorization by job type
- **TF-IDF Vectorizer**: Text feature extraction
- **Cosine Similarity**: Resume-job description matching

## Project Structure

```
resume-checker/
├── backend/                          # Python Flask API
│   ├── app.py                      # Flask application & endpoints
│   ├── requirements.txt             # Python dependencies
│   ├── models/                      # Trained ML models
│   │   ├── svm_model.pkl
│   │   └── tfidf_vectorizer.pkl
│   ├── notebooks/                   # Jupyter notebooks
│   │   └── train_model.ipynb        # SVM training notebook
│   └── utils/                       # Utility modules
│       ├── file_parser.py           # Document parsing
│       ├── text_processor.py        # NLP processing
│       └── evaluation.py            # Resume analysis
│
└── frontend/                         # Next.js React App
    ├── package.json
    ├── next.config.js
    ├── pages/                       # API routes & pages
    │   ├── index.js                # Main application
    │   ├── _app.js                 # App wrapper
    │   └── _document.js            # HTML document
    ├── components/                  # React components
    │   ├── FileUploader.js          # File upload with drag-drop
    │   └── ResultsDisplay.js        # Results visualization
    ├── lib/                         # Utilities
    │   └── api.js                   # API client
    ├── styles/                      # CSS
    │   └── globals.css              # Global styles
    └── public/                      # Static files
```

## Setup Instructions

### Backend Setup

#### Prerequisites
- Python 3.8+
- pip (Python package manager)

#### Installation

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data**
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

5. **Train the SVM Model (First Time)**
   - Open `notebooks/train_model.ipynb` in Jupyter
   - Run all cells to train the SVM model and vectorizer
   - This will generate `models/svm_model.pkl` and `models/tfidf_vectorizer.pkl`

   ```bash
   jupyter notebook notebooks/train_model.ipynb
   ```

6. **Start the Flask API**
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

### Frontend Setup

#### Prerequisites
- Node.js 14+ and npm

#### Installation

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Create .env.local file**
   ```bash
   # .env.local
   NEXT_PUBLIC_API_URL=http://localhost:5000
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```
   The application will be available at `http://localhost:3000`

## Usage

### 1. Text Input
1. Go to the "📝 Text Input" tab
2. Paste your resume content
3. Paste the job description
4. Click "🔍 Analyze Resume"

### 2. File Upload
1. Go to the "📄 File Upload" tab
2. Drag and drop or click to select a resume file (.txt, .pdf, or .docx)
3. Paste the job description
4. Click "🔍 Analyze Resume"

### 3. View Results
The analysis displays:
- **Overall Match Score**: Percentage based on all metrics
- **Grammar & Readability**: Word count and Flesch score interpretation
- **Keyword Match**: Matched and missing keywords with match percentage
- **ATS Compatibility**: ATS-friendliness score and level
- **Skills Gap Analysis**: Found, missing, and all detected skills
- **Recommendations**: Actionable suggestions for improvement

## API Endpoints

### Health Check
- **GET** `/health`
- Response: API status

### Analyze Resume
- **POST** `/api/analyze`
- Accepts: `resume_text` or `resume_file`, `job_description`
- Returns: Comprehensive analysis object

### Match Resume
- **POST** `/api/match`
- Accepts: JSON with `resume_text`, `job_description`
- Returns: Match scores and gap analysis

### Upload File
- **POST** `/api/file-upload`
- Accepts: Form data with `file`
- Returns: Extracted text content

### Classify Resume
- **POST** `/api/classify`
- Accepts: JSON with `resume_text`
- Returns: SVM classification result

## Model Training Details

The Jupyter Notebook (`train_model.ipynb`) includes:

1. **Data Loading**: Resume dataset exploration
2. **Text Preprocessing**: Cleaning, tokenization, stopword removal
3. **Feature Extraction**: TF-IDF vectorization
4. **SVM Training**: Classification model training and evaluation
5. **Evaluation Metrics**: Accuracy, Precision, Recall, F1-score
6. **File Parsing**: Multi-format document handling
7. **Readability Metrics**: Flesch Kincaid calculations
8. **Skills Gap Analysis**: Skill extraction and comparison
9. **Model Persistence**: Saving trained models for production

## Configuration

### Environment Variables

**Frontend (.env.local)**
```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

**Backend**
- Upload folder: `temp/resume_uploads`
- Max file size: 10MB
- Allowed extensions: txt, pdf, docx

## Performance Notes

- TF-IDF vectorization is performed on the fly during analysis
- Cosine similarity provides instant matching results
- File parsing handles documents up to 10MB
- Average analysis time: 1-2 seconds

## Technical Stack

### Backend
- **Framework**: Flask 2.3+
- **NLP**: NLTK, scikit-learn
- **ML**: SVM, TF-IDF, Cosine Similarity
- **Readability**: textstat
- **File Handling**: PyPDF2, python-docx

### Frontend
- **Framework**: Next.js 13+
- **UI**: React 18+
- **HTTP Client**: Axios
- **File Upload**: react-dropzone
- **Styling**: CSS3

## Troubleshooting

### CORS Issues
If you get CORS errors, ensure the backend is running with `CORS(app)` enabled in `app.py`.

### Models Not Found
Train the model first by running all cells in `train_model.ipynb`.

### API Connection Issues
1. Verify Flask server is running on port 5000
2. Check firewall settings
3. Confirm `NEXT_PUBLIC_API_URL` is correctly set

### File Upload Issues
- Ensure file size is under 10MB
- Only .txt, .pdf, .docx files are supported
- Check browser console for specific errors

## Future Enhancements

- [ ] Machine Learning model improvement
- [ ] Support for more document formats
- [ ] Resume templates and suggestions
- [ ] Interview preparation tips
- [ ] Salary range analysis
- [ ] Cover letter analysis
- [ ] Multi-language support
- [ ] Dark mode UI

## License

This project is open source and available under the MIT License.

## Support

For issues, suggestions, or contributions, please reach out to the development team.

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Made with ❤️ for better resume and job matching**
