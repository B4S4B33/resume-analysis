# Resume Checker - Testing & Deployment Guide

## Unit Testing

### Backend Testing with pytest

```bash
cd backend
pip install pytest pytest-cov
pytest --cov=.
```

### Frontend Testing with Jest

```bash
cd frontend
npm install --save-dev jest @testing-library/react
npm test
```

## Integration Testing

### API Endpoints Testing

**1. Health Check**
```bash
curl -X GET http://localhost:5000/health
```

Expected Response:
```json
{
  "status": "healthy",
  "service": "Resume Checker API",
  "version": "1.0.0"
}
```

**2. Analyze Resume (Text)**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "resume_text=Python developer with 5 years experience" \
  -F "job_description=We need a senior Python developer"
```

**3. Analyze Resume (File)**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "resume_file=@resume.pdf" \
  -F "job_description=We need a senior Python developer"
```

**4. Match Resume (JSON)**
```bash
curl -X POST http://localhost:5000/api/match \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Python Flask Django REST API",
    "job_description": "Senior Python developer needed"
  }'
```

**5. File Upload**
```bash
curl -X POST http://localhost:5000/api/file-upload \
  -F "file=@resume.txt"
```

**6. Classify Resume**
```bash
curl -X POST http://localhost:5000/api/classify \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Senior Software Engineer with Python expertise"
  }'
```

## Load Testing

### Using Apache Bench
```bash
ab -n 100 -c 10 http://localhost:5000/health
```

### Using wrk
```bash
wrk -t4 -c100 -d30s --script=post.lua http://localhost:5000/api/analyze
```

## Browser Testing

### Chrome DevTools
1. Open DevTools (F12)
2. Check Network tab for API calls
3. Monitor Console for errors
4. Check Performance for load times

### User Testing Scenarios

**Scenario 1: Text Input Analysis**
- Open http://localhost:3000
- Click "📝 Text Input"
- Paste sample resume and job description
- Verify all metrics display correctly

**Scenario 2: File Upload**
- Click "📄 File Upload"
- Upload a PDF resume
- Add job description
- Verify file is processed correctly

**Scenario 3: Sample Data**
- Click "📚 Load Sample Data"
- Click "🔍 Analyze Resume"
- Verify results display

**Scenario 4: Error Handling**
- Try submitting without job description
- Verify error message appears
- Try uploading invalid file
- Verify error handling works

## Performance Testing

### API Response Times

Expected response times:
- Health check: < 100ms
- Analyze resume (text): 1-2 seconds
- File upload + analysis: 2-3 seconds
- Classification: 500-1000ms

### Memory Usage

Monitor with:
```bash
# Backend
python -m memory_profiler app.py

# Frontend
npm run build
npm start
```

## Security Testing

### CORS Headers
```bash
curl -i -X OPTIONS http://localhost:5000/health
```

### File Upload Validation
- Invalid file type: Should reject
- File > 10MB: Should reject
- Valid file: Should accept and parse

### Input Validation
- Empty strings: Should show error
- Null values: Should handle gracefully
- Special characters: Should sanitize

## Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] No console errors
- [ ] Load test successful
- [ ] Security audit passed
- [ ] Documentation complete

### Deployment Steps

**1. Prepare Backend**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**2. Prepare Frontend**
```bash
cd frontend
npm install
npm run build
npm start
```

**3. Verify Connections**
- Test all API endpoints
- Check frontend-backend communication
- Verify uploads work

**4. Monitor**
```bash
# Check logs
tail -f backend.log
tail -f frontend.log
```

## Production Deployment

### Using Gunicorn (Backend)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using PM2 (Frontend)
```bash
npm install -g pm2
pm2 start "npm start" --name "resume-checker"
```

### Nginx Reverse Proxy

```nginx
upstream backend {
    server 127.0.0.1:5000;
}

upstream frontend {
    server 127.0.0.1:3000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location /api {
        proxy_pass http://backend;
    }

    location / {
        proxy_pass http://frontend;
    }
}
```

## Monitoring & Logging

### Backend Logging
```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Frontend Error Tracking
```javascript
// Add error tracking
window.addEventListener('error', (event) => {
    console.error('Frontend error:', event.error);
});
```

## Database Optimization (Future)

When adding a database:
- Index frequently searched fields
- Implement caching for analysis results
- Archive old analyses

## Backup Strategy

- Daily backup of trained models
- Weekly backup of database
- Version control for all code

## Troubleshooting

### Common Issues

1. **Port Already in Use**
```bash
# Kill process on port
lsof -i :5000
kill -9 <PID>
```

2. **Memory Leak**
```bash
# Monitor memory
watch -n 1 'ps aux | grep python'
```

3. **API Timeout**
- Increase timeout in frontend api.js
- Check backend logs for slow queries

4. **File Upload Fails**
- Check file permissions
- Verify temp directory exists
- Check disk space

## Performance Optimization

1. **Enable Caching**
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

2. **Compress Responses**
```python
from flask_compress import Compress
Compress(app)
```

3. **Optimize ML Models**
- Use model quantization
- Implement lazy loading
- Cache vectorizer results

4. **Frontend Optimization**
```bash
npm run build --analyze
```

---

## References

- Flask Documentation: https://flask.palletsprojects.com/
- Next.js Documentation: https://nextjs.org/docs
- scikit-learn Documentation: https://scikit-learn.org/
- Testing Best Practices: https://testing-library.com/

---

Ready to deploy? Follow this guide for a smooth production release!
