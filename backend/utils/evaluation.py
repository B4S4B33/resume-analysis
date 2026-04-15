"""
Resume evaluation module that combines all analysis
"""
from typing import Dict, Any
from .text_processor import (
    clean_text,
    calculate_word_count,
    calculate_flesch_score,
    calculate_keyword_match,
    calculate_ats_compatibility,
    extract_skills,
    calculate_skills_gap
)


def evaluate_resume(resume_text: str, job_description: str) -> Dict[str, Any]:
    """
    Comprehensive resume evaluation
    Returns evaluation metrics and recommendations
    """
    # Clean texts
    resume_clean = clean_text(resume_text)
    job_clean = clean_text(job_description)
    
    # Grammar & Readability
    word_count = calculate_word_count(resume_clean)
    flesch_score = calculate_flesch_score(resume_text)
    
    # Keyword Match
    keyword_match_score, matched_keywords, missing_keywords = calculate_keyword_match(
        resume_clean, job_clean
    )
    
    # ATS Compatibility
    ats_score = calculate_ats_compatibility(resume_text)
    
    # Skills Gap Analysis
    found_skills, missing_skills = calculate_skills_gap(resume_clean, job_clean)
    
    # Extract all skills found in resume
    resume_skills = extract_skills(resume_clean)
    
    # Generate recommendations
    recommendations = generate_recommendations(
        word_count, flesch_score, keyword_match_score, ats_score, missing_keywords, missing_skills
    )
    
    return {
        "grammar_readability": {
            "word_count": word_count,
            "flesch_score": round(flesch_score, 2),
            "readability_level": get_readability_level(flesch_score)
        },
        "keyword_match": {
            "score": round(keyword_match_score, 2),
            "matched_keywords": matched_keywords[:10],  # Top 10
            "missing_keywords": missing_keywords[:10],   # Top 10
            "match_percentage": round(len(matched_keywords) / max(1, len(matched_keywords) + len(missing_keywords)) * 100, 2)
        },
        "ats_compatibility": {
            "score": round(ats_score, 2),
            "level": get_ats_level(ats_score)
        },
        "skills_gap": {
            "found_skills": found_skills,
            "missing_skills": missing_skills,
            "all_detected_skills": resume_skills,
            "gap_percentage": round(len(missing_skills) / max(1, len(found_skills) + len(missing_skills)) * 100, 2)
        },
        "overall_score": round((keyword_match_score + ats_score + (100 - (len(missing_skills) / max(1, len(found_skills) + len(missing_skills)) * 100))) / 3, 2),
        "recommendations": recommendations
    }


def get_readability_level(flesch_score: float) -> str:
    """Get readability level description"""
    if flesch_score >= 90:
        return "Extremely Easy"
    elif flesch_score >= 80:
        return "Very Easy"
    elif flesch_score >= 70:
        return "Easy"
    elif flesch_score >= 60:
        return "Fairly Easy"
    elif flesch_score >= 50:
        return "Standard"
    elif flesch_score >= 30:
        return "Difficult"
    else:
        return "Very Difficult"


def get_ats_level(ats_score: float) -> str:
    """Get ATS compatibility level"""
    if ats_score >= 80:
        return "Excellent"
    elif ats_score >= 60:
        return "Good"
    elif ats_score >= 40:
        return "Fair"
    else:
        return "Poor"


def generate_recommendations(word_count: int, flesch_score: float, keyword_match: float, 
                            ats_score: float, missing_keywords: list, missing_skills: list) -> list:
    """Generate actionable recommendations"""
    recommendations = []
    
    # Word count recommendations
    if word_count < 200:
        recommendations.append("Add more content to your resume (currently too short)")
    elif word_count > 1000:
        recommendations.append("Your resume is quite long; try to be more concise")
    
    # Readability recommendations
    if flesch_score < 50:
        recommendations.append("Simplify the language used in your resume for better readability")
    
    # Keyword recommendations
    if keyword_match < 50:
        recommendations.append(f"Incorporate more job-specific keywords: {', '.join(missing_keywords[:5])}")
    
    # ATS recommendations
    if ats_score < 70:
        recommendations.append("Improve ATS compatibility by using standard formatting and avoiding special characters")
    
    # Skills recommendations
    if missing_skills:
        recommendations.append(f"Consider adding these important skills: {', '.join(missing_skills[:5])}")
    
    if not recommendations:
        recommendations.append("Your resume looks great!")
    
    return recommendations
