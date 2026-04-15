import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import apiService from '../lib/api';
import FileUploader from '../components/FileUploader';
import ResultsDisplay from '../components/ResultsDisplay';

export default function Home() {
  const [activeTab, setActiveTab] = useState('text');
  const [jobTab, setJobTab] = useState('text');
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [jobFile, setJobFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [apiStatus, setApiStatus] = useState('unknown');

  // Check API health on mount
  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      await apiService.healthCheck();
      setApiStatus('connected');
    } catch (err) {
      setApiStatus('disconnected');
      console.error('API health check failed:', err);
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    setResults(null);

    // Validation
    if (jobTab === 'text' && !jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    if (jobTab === 'file' && !jobFile) {
      setError('Please select a job description file');
      return;
    }

    if (activeTab === 'text' && !resumeText.trim()) {
      setError('Please enter resume text');
      return;
    }

    if (activeTab === 'file' && !resumeFile) {
      setError('Please select a resume file');
      return;
    }

    setLoading(true);

    try {
      let result;
      const jobDesc = jobTab === 'text' ? jobDescription : null;
      
      if (activeTab === 'text') {
        result = await apiService.analyzeResume(resumeText, jobDesc, null, jobFile);
      } else {
        result = await apiService.analyzeResume('', jobDesc, resumeFile, jobFile);
      }

      if (result.success) {
        setResults(result.analysis);
        setSuccess('Resume analysis completed successfully!');
      } else {
        setError(result.error || 'Analysis failed');
      }
    } catch (err) {
      const errorMessage =
        err.response?.data?.error ||
        err.message ||
        'Failed to analyze resume. Please check your connection and try again.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (file) => {
    setResumeFile(file);
    setResumeText('');
  };

  const handleJobFileSelect = (file) => {
    setJobFile(file);
    setJobDescription('');
  };

  const handleClearAll = () => {
    setResumeText('');
    setResumeFile(null);
    setJobDescription('');
    setJobFile(null);
    setResults(null);
    setError(null);
    setSuccess(null);
  };

  const handleLoadSampleData = () => {
    setResumeText(
      `Senior Software Engineer
      
Experience:
- 5+ years of full-stack web development
- Expertise in Python, JavaScript, React, Django, Flask
- Strong experience with REST APIs, microservices, Docker, Kubernetes
- AWS and Azure cloud platform expertise
- CI/CD pipeline development with Jenkins and GitLab CI
- SQL and NoSQL database design and optimization

Skills:
Python, JavaScript, React, Node.js, Django, Flask, Express, MongoDB, PostgreSQL, 
Docker, Kubernetes, AWS, Azure, Git, Linux, Jenkins, CI/CD, Microservices, REST APIs

Education:
Bachelor of Science in Computer Science
GPA: 3.8/4.0`
    );

    setJobDescription(
      `We are looking for a Senior Python Developer with the following qualifications:

Required Skills:
- 5+ years of Python development experience
- Strong expertise in Django and Flask frameworks
- Experience with REST API development
- Proficiency in SQL and NoSQL databases
- Docker and Kubernetes knowledge
- AWS cloud platform experience
- Git version control
- Linux/Unix system administration

Nice to Have:
- Experience with microservices architecture
- CI/CD pipeline experience
- Machine Learning knowledge
- React or Angular frontend experience
- DevOps experience`
    );
  };

  return (
    <>
      <Head>
        <title>Resume Checker - AI-Powered Resume Analysis</title>
        <meta name="description" content="Analyze and optimize your resume" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="container" style={{ marginTop: '30px' }}>
        {/* Header */}
        <div className="card" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', textAlign: 'center' }}>
          <h1 style={{ fontSize: '2.5em', marginBottom: '10px' }}>📋 Resume Checker</h1>
          <p style={{ fontSize: '1.1em', marginBottom: 0 }}>
            AI-Powered Resume Analysis & Job Matching
          </p>
          <p style={{ fontSize: '0.9em', opacity: 0.9, marginTop: '10px' }}>
            API Status:{' '}
            <span
              style={{
                color: apiStatus === 'connected' ? '#28a745' : '#f5a623',
                fontWeight: 'bold',
              }}
            >
              {apiStatus === 'connected' ? '✓ Connected' : '⚠ Connecting...'}
            </span>
          </p>
        </div>

        {/* Alerts */}
        {error && (
          <div className="alert alert-error">
            <strong>Error:</strong> {error}
          </div>
        )}
        {success && (
          <div className="alert alert-success">
            <strong>Success:</strong> {success}
          </div>
        )}

        {/* Main Form */}
        <div className="card">
          <form onSubmit={handleAnalyze}>
            {/* Input Tabs */}
            <div className="tabs">
              <button
                type="button"
                className={`tab-button ${activeTab === 'text' ? 'active' : ''}`}
                onClick={() => {
                  setActiveTab('text');
                  setResumeFile(null);
                  setError(null);
                }}
              >
                📝 Text Input
              </button>
              <button
                type="button"
                className={`tab-button ${activeTab === 'file' ? 'active' : ''}`}
                onClick={() => {
                  setActiveTab('file');
                  setResumeText('');
                  setError(null);
                }}
              >
                📄 File Upload
              </button>
            </div>

            {/* Resume Input */}
            <div className={`tab-content ${activeTab === 'text' ? 'active' : ''}`}>
              <div className="form-group">
                <label htmlFor="resume">Your Resume</label>
                <textarea
                  id="resume"
                  value={resumeText}
                  onChange={(e) => setResumeText(e.target.value)}
                  placeholder="Paste your resume content here..."
                  disabled={loading}
                />
              </div>
            </div>

            <div className={`tab-content ${activeTab === 'file' ? 'active' : ''}`}>
              <FileUploader onFileSelect={handleFileSelect} disabled={loading} />
            </div>

            {/* Job Description */}
            <div className="form-group">
              <label>Job Description</label>
              <div className="tabs">
                <button
                  type="button"
                  className={`tab-button ${jobTab === 'text' ? 'active' : ''}`}
                  onClick={() => {
                    setJobTab('text');
                    setJobFile(null);
                    setError(null);
                  }}
                >
                  📝 Text Input
                </button>
                <button
                  type="button"
                  className={`tab-button ${jobTab === 'file' ? 'active' : ''}`}
                  onClick={() => {
                    setJobTab('file');
                    setJobDescription('');
                    setError(null);
                  }}
                >
                  📄 File Upload
                </button>
              </div>
            </div>

            <div className={`tab-content ${jobTab === 'text' ? 'active' : ''}`}>
              <div className="form-group">
                <textarea
                  id="jobDesc"
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  placeholder="Paste the job description here..."
                  disabled={loading}
                />
              </div>
            </div>

            <div className={`tab-content ${jobTab === 'file' ? 'active' : ''}`}>
              <FileUploader 
                onFileSelect={handleJobFileSelect} 
                disabled={loading}
                label="Select Job Description File"
              />
            </div>

            {/* Buttons */}
            <button type="submit" className="btn btn-primary" disabled={loading || apiStatus !== 'connected'}>
              {loading ? (
                <>
                  <span className="loading"></span> Analyzing...
                </>
              ) : (
                '🔍 Analyze Resume'
              )}
            </button>

            <button
              type="button"
              className="btn btn-secondary"
              onClick={handleLoadSampleData}
              disabled={loading}
            >
              📚 Load Sample Data
            </button>

            {(resumeText || resumeFile || jobDescription || jobFile) && (
              <button
                type="button"
                className="btn btn-secondary"
                onClick={handleClearAll}
                disabled={loading}
              >
                🗑️ Clear All
              </button>
            )}
          </form>
        </div>

        {/* Results */}
        {results && <ResultsDisplay analysis={results} loading={false} />}

        {/* Footer */}
        <div
          style={{
            textAlign: 'center',
            color: 'white',
            padding: '30px 20px',
            marginTop: '40px',
          }}
        >
          <p>
            Made with ❤️ | Resume Checker v1.0 | NLP Project
          </p>
          <p style={{ fontSize: '0.9em', opacity: 0.8 }}>
            Powered by TF-IDF, Cosine Similarity & SVM Classification
          </p>
        </div>
      </div>
    </>
  );
}
