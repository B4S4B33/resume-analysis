# Resume Checker - Docker Support (Optional)

## Docker Deployment

### Build Backend Image
```bash
cd backend
docker build -t resume-checker-backend .
docker run -p 5000:5000 resume-checker-backend
```

### Build Frontend Image
```bash
cd frontend
docker build -t resume-checker-frontend .
docker run -p 3000:3000 resume-checker-frontend
```

### Docker Compose
```bash
docker-compose up
```

Both services will be available:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

---

## File Structure for Docker

Create these Dockerfile files in respective directories:

### backend/Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt && \
    python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

COPY . .

CMD ["python", "app.py"]
```

### frontend/Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

ENV NEXT_PUBLIC_API_URL=http://backend:5000

RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

### docker-compose.yml (root directory)
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app
    environment:
      - FLASK_ENV=development

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:5000
```
