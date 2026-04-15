"""
Text processing utilities for resume analysis
"""
import re
from typing import List, Tuple
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import textstat
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


def clean_text(text: str) -> str:
    """Clean and preprocess text"""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and extra whitespace
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\-]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_keywords(text: str, n_keywords: int = 20) -> List[str]:
    """Extract top keywords from text"""
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    
    # Filter stopwords and short tokens
    keywords = [token for token in tokens 
                if token.isalpha() and token not in stop_words and len(token) > 2]
    
    # Count frequency
    from collections import Counter
    freq_dist = Counter(keywords)
    top_keywords = [word for word, _ in freq_dist.most_common(n_keywords)]
    
    return top_keywords


def calculate_word_count(text: str) -> int:
    """Calculate word count"""
    return len(text.split())


def calculate_flesch_score(text: str) -> float:
    """
    Calculate Flesch Reading Ease Score
    0-30: Very Difficult, 30-50: Difficult, 50-60: Standard,
    60-70: Fairly Easy, 70-80: Easy, 80-90: Very Easy, 90-100: Extremely Easy
    """
    try:
        score = textstat.flesch_reading_ease(text)
        return max(0, min(100, score))  # Clamp between 0-100
    except:
        return 50.0


def calculate_keyword_match(resume_text: str, job_description: str) -> Tuple[float, List[str], List[str]]:
    """
    Calculate keyword match between resume and job description using TF-IDF and Cosine Similarity
    Returns: (match_score, matched_keywords, missing_keywords)
    """
    try:
        # Vectorize documents
        vectorizer = TfidfVectorizer(max_features=100, lowercase=True)
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
        
        # Calculate cosine similarity
        similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        match_score = float(similarity_score * 100)
        
        # Extract keywords
        resume_keywords = set(extract_keywords(resume_text, n_keywords=15))
        job_keywords = set(extract_keywords(job_description, n_keywords=15))
        
        matched_keywords = list(resume_keywords & job_keywords)
        missing_keywords = list(job_keywords - resume_keywords)
        
        return match_score, matched_keywords, missing_keywords
    except Exception as e:
        print(f"Error in keyword match: {str(e)}")
        return 0.0, [], []


def calculate_ats_compatibility(text: str) -> float:
    """
    Calculate ATS (Applicant Tracking System) compatibility score
    ATS prefers: simple formatting, standard fonts, clear sections, no images/tables
    """
    score = 100.0
    
    # Check for proper formatting (simple sections and keywords)
    section_keywords = ['experience', 'skills', 'education', 'projects', 'certifications']
    found_sections = sum(1 for keyword in section_keywords if keyword in text.lower())
    score += found_sections * 5
    
    # Deduct for uncommon special characters that ATS might struggle with
    special_chars = len(re.findall(r'[^\w\s\.\,\-\:]', text))
    score -= min(20, special_chars * 0.5)
    
    # Bonus for standard formatting
    if any(contact in text.lower() for contact in ['email', 'phone', 'linkedin']):
        score += 10
    
    # Normalize score to 0-100
    score = max(0, min(100, score))
    return float(score)


def extract_skills(text: str) -> List[str]:
    """
    Extract skills from text
    Looks for common skill markers and keywords
    """
    common_skills = {
        'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'kotlin'],
        'web': ['html', 'css', 'react', 'angular', 'vue', 'node', 'express', 'flask', 'django', 'asp.net'],
        'data': ['sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'elasticsearch', 'spark', 'hadoop'],
        'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'ci/cd', 'jenkins'],
        'data_science': ['pandas', 'numpy', 'sklearn', 'tensorflow', 'pytorch', 'ml', 'deep learning', 'nlp'],
        'tools': ['git', 'linux', 'windows', 'mac', 'vim', 'vscode', 'jira', 'confluence']
    }
    
    text_lower = text.lower()
    found_skills = []
    
    for category, skills in common_skills.items():
        for skill in skills:
            if skill in text_lower:
                found_skills.append(skill)
    
    return list(set(found_skills))


def calculate_skills_gap(resume_text: str, job_description: str) -> Tuple[List[str], List[str]]:
    """
    Calculate skills gap between resume and job description
    Returns: (found_skills, missing_skills)
    """
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))
    
    found_skills = list(resume_skills & job_skills)
    missing_skills = list(job_skills - resume_skills)
    
    return found_skills, missing_skills
