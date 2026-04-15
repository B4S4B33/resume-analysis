# Architecture Decision Records

## ADR-001: Framework Choice

### Context
We needed to build a web application with Python backend and JavaScript frontend.

### Decision
- **Backend**: Flask (lightweight, flexible, easy to extend)
- **Frontend**: Next.js (React-based, SSR, excellent performance)

### Consequences
- Fast development cycle
- Easy deployment
- Scalable architecture
- Good community support

---

## ADR-002: ML Model Selection

### Context
We needed to classify resumes and match them against job descriptions.

### Decision
- **Classification**: Support Vector Machine (SVM) with TF-IDF
- **Matching**: Cosine Similarity
- **Text Processing**: NLTK

### Consequences
- Fast inference time
- Good accuracy with reasonable data
- Interpretable results
- Easy to retrain with new data

---

## ADR-003: File Format Support

### Context
Users need to upload resumes in multiple formats.

### Decision
- Support: .txt, .pdf, .docx
- Max file size: 10MB
- Validation on both client and server

### Consequences
- Better UX
- More flexibility
- Requires multiple parsing libraries

---

## ADR-004: API Design

### Context
Need to expose ML functionality through REST endpoints.

### Decision
- RESTful API design
- JSON for data exchange
- Multipart form data for file uploads
- Comprehensive error handling

### Consequences
- Standard, easy to understand
- compatible with frontend frameworks
- Easy to extend

---

## ADR-005: Data Flow

### Context
Resume data needs to flow from frontend to backend and back.

### Decision
- Frontend collects data
- Backend processes (parsing, vectorization, analysis)
- Results returned as JSON
- Frontend displays rich visualizations

### Consequences
- Clear separation of concerns
- Scalable architecture
- Easy to add features

---

## ADR-006: Deployment Strategy

### Context
Need to deploy both frontend and backend services.

### Decision
- Docker containerization (optional)
- Separate processes for backend and frontend
- Environment-based configuration
- CORS enabled for flexibility

### Consequences
- Easy scaling
- Simple deployment
- Good development experience
