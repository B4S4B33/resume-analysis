# Resume Checker - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Step 1: Train the ML Model (One-time setup)

```bash
cd backend
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
jupyter notebook notebooks/train_model.ipynb
```

In the Jupyter notebook, run all cells to train and save the SVM model.

### Step 2: Start the Backend

```bash
python app.py
```

✅ Backend running at: `http://localhost:5000`

### Step 3: Start the Frontend (in a new terminal)

```bash
cd frontend
npm install
npm run dev
```

✅ Frontend running at: `http://localhost:3000`

### Step 4: Open in Browser

Visit `http://localhost:3000` and start analyzing resumes!

---

## 📋 What the App Does

### Input Options
- **Text**: Paste resume and job description directly
- **File**: Upload .txt, .pdf, or .docx files

### Analysis Output
1. **Overall Match Score** - Percentage match between resume and job
2. **Grammar & Readability** - Word count and Flesch reading score
3. **Keyword Match** - Keywords found and missing
4. **ATS Compatibility** - How well the resume will pass ATS systems
5. **Skills Gap** - Skills you have vs. skills needed
6. **Recommendations** - Actionable improvement suggestions

---

## 🔧 Technology Stack

### Backend
- **Python Flask** - REST API
- **scikit-learn** - SVM model training
- **NLTK** - NLP processing
- **PyPDF2, python-docx** - Document parsing

### Frontend
- **Next.js** - React framework
- **Axios** - API communication
- **react-dropzone** - File uploads
- **CSS3** - Styling

---

## 📝 Example Usage

### Via Text Input
1. Click "📝 Text Input" tab
2. Paste your resume in the first box
3. Paste job description in the second box
4. Click "🔍 Analyze Resume"
5. View the comprehensive analysis

### Via File Upload
1. Click "📄 File Upload" tab
2. Drag and drop your PDF/DOCX/TXT file
3. Paste the job description
4. Click "🔍 Analyze Resume"

### Load Sample Data
Click "📚 Load Sample Data" to see how the app works with example content.

---

## 💡 Key Features

✅ **AI-Powered Analysis**
- SVM machine learning classification
- TF-IDF text vectorization
- Cosine similarity matching

✅ **Multiple File Formats**
- Text (.txt)
- PDF (.pdf)
- Word (.docx)

✅ **Comprehensive Metrics**
- Readability analysis
- Keyword extraction
- ATS compatibility scoring
- Skills gap identification

✅ **Real-time Feedback**
- Instant analysis results
- Actionable recommendations
- Visual score representations

---

## 🐛 Troubleshooting

### "API connection error"
- Make sure backend is running (`python app.py`)
- Check if port 5000 is accessible
- Restart both frontend and backend

### "Models not found"
- Run the Jupyter notebook to train the SVM
- Check if `models/` folder has .pkl files

### "File upload not working"
- Only .txt, .pdf, .docx supported
- Max file size is 10MB

### "CORS errors"
- Backend already has CORS enabled
- Clear browser cache and reload

---

## 📚 Project Structure

```
resume-checker/
├── backend/
│   ├── app.py                  (Flask API)
│   ├── requirements.txt         (Dependencies)
│   ├── models/                  (Trained models)
│   ├── notebooks/train_model.ipynb
│   └── utils/                   (Helper modules)
│
└── frontend/
    ├── pages/index.js           (Main UI)
    ├── components/              (React components)
    ├── styles/globals.css       (Styling)
    └── package.json
```

---

## 🎯 Next Steps

- Load sample data to understand the features
- Try with real resume and job descriptions
- Check recommendations for improvement
- Modify resume based on suggestions
- Re-analyze to see improvements

---

## 📞 Support

For detailed setup instructions, see:
- Backend: `backend/SETUP.md`
- Frontend: `frontend/SETUP.md`

Main documentation: `README.md`

---

Made with ❤️ for better resume and job matching
