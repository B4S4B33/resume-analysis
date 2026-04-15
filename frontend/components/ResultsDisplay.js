import React from 'react';

export default function ResultsDisplay({ analysis, loading = false }) {
  if (loading) {
    return (
      <div className="card">
        <p style={{ textAlign: 'center', padding: '20px' }}>
          <span className="loading"></span> Analyzing resume...
        </p>
      </div>
    );
  }

  if (!analysis) {
    return null;
  }

  const {
    grammar_readability = {},
    keyword_match = {},
    ats_compatibility = {},
    skills_gap = {},
    overall_score = 0,
    recommendations = [],
  } = analysis;

  const getScoreColor = (score) => {
    if (score >= 80) return '#28a745';
    if (score >= 60) return '#ffc107';
    if (score >= 40) return '#fd7e14';
    return '#dc3545';
  };

  const getScoreLevel = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Poor';
  };

  return (
    <div className="container">
      {/* Overall Score */}
      <div className="card">
        <div className="card-title">Overall Match Score</div>
        <div
          style={{
            textAlign: 'center',
            fontSize: '3em',
            fontWeight: 'bold',
            color: getScoreColor(overall_score),
            marginBottom: '10px',
          }}
        >
          {overall_score.toFixed(1)}%
        </div>
        <p style={{ textAlign: 'center', color: '#666', marginBottom: '15px' }}>
          {getScoreLevel(overall_score)} Match
        </p>
        <div className="score-bar">
          <div
            className="score-fill"
            style={{
              width: `${overall_score}%`,
              backgroundColor: getScoreColor(overall_score),
            }}
          >
            {overall_score > 10 && `${overall_score.toFixed(1)}%`}
          </div>
        </div>
      </div>

      {/* Grammar & Readability */}
      <div className="card">
        <div className="card-title">📝 Grammar & Readability</div>
        <div className="results-grid">
          <div className="result-item">
            <div className="result-item-title">Word Count</div>
            <div className="result-item-value">{grammar_readability.word_count || 0}</div>
            <div className="result-item-label">Words</div>
          </div>
          <div className="result-item">
            <div className="result-item-title">Flesch Score</div>
            <div className="result-item-value">
              {(grammar_readability.flesch_score || 0).toFixed(1)}
            </div>
            <div className="result-item-label">
              {grammar_readability.readability_level || 'Unknown'}
            </div>
          </div>
        </div>
      </div>

      {/* Keyword Match */}
      <div className="card">
        <div className="card-title">🔑 Keyword Match</div>
        <div style={{ marginBottom: '15px' }}>
          <div className="score-bar">
            <div
              className="score-fill"
              style={{ width: `${keyword_match.score || 0}%` }}
            >
              {keyword_match.score > 10 && `${keyword_match.score.toFixed(1)}%`}
            </div>
          </div>
          <p style={{ marginTop: '10px', color: '#666' }}>
            Match Percentage: {(keyword_match.match_percentage || 0).toFixed(1)}%
          </p>
        </div>

        {keyword_match.matched_keywords && keyword_match.matched_keywords.length > 0 && (
          <div>
            <h4 style={{ marginTop: '15px', marginBottom: '8px', color: '#333' }}>
              ✓ Matched Keywords
            </h4>
            <ul className="skills-list">
              {keyword_match.matched_keywords.map((keyword, idx) => (
                <li key={idx}>{keyword}</li>
              ))}
            </ul>
          </div>
        )}

        {keyword_match.missing_keywords && keyword_match.missing_keywords.length > 0 && (
          <div>
            <h4 style={{ marginTop: '15px', marginBottom: '8px', color: '#e74c3c' }}>
              ✗ Missing Keywords
            </h4>
            <ul className="skills-list gap">
              {keyword_match.missing_keywords.map((keyword, idx) => (
                <li key={idx}>{keyword}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* ATS Compatibility */}
      <div className="card">
        <div className="card-title">🤖 ATS Compatibility</div>
        <div
          style={{
            fontSize: '2.5em',
            fontWeight: 'bold',
            color: getScoreColor(ats_compatibility.score || 0),
            marginBottom: '10px',
          }}
        >
          {(ats_compatibility.score || 0).toFixed(1)}%
        </div>
        <p style={{ marginBottom: '15px', color: '#666' }}>
          ATS Level: <strong>{ats_compatibility.level || 'Unknown'}</strong>
        </p>
        <div className="score-bar">
          <div
            className="score-fill"
            style={{
              width: `${ats_compatibility.score || 0}%`,
              backgroundColor: getScoreColor(ats_compatibility.score || 0),
            }}
          >
            {ats_compatibility.score > 10 && `${(ats_compatibility.score || 0).toFixed(1)}%`}
          </div>
        </div>
      </div>

      {/* Skills Gap Analysis */}
      <div className="card">
        <div className="card-title">💡 Skills Gap Analysis</div>

        {skills_gap.found_skills && skills_gap.found_skills.length > 0 && (
          <div>
            <h4 style={{ marginBottom: '8px', color: '#28a745' }}>Found Skills</h4>
            <ul className="skills-list">
              {skills_gap.found_skills.map((skill, idx) => (
                <li key={idx}>{skill}</li>
              ))}
            </ul>
          </div>
        )}

        {skills_gap.missing_skills && skills_gap.missing_skills.length > 0 && (
          <div>
            <h4 style={{ marginTop: '15px', marginBottom: '8px', color: '#e74c3c' }}>
              Skills to Develop (Priority)
            </h4>
            <ul className="skills-list gap">
              {skills_gap.missing_skills.map((skill, idx) => (
                <li key={idx}>{skill}</li>
              ))}
            </ul>
          </div>
        )}

        {skills_gap.all_detected_skills && skills_gap.all_detected_skills.length > 0 && (
          <div>
            <h4 style={{ marginTop: '15px', marginBottom: '8px', color: '#667eea' }}>
              All Detected Skills
            </h4>
            <ul className="skills-list">
              {skills_gap.all_detected_skills.map((skill, idx) => (
                <li key={idx}>{skill}</li>
              ))}
            </ul>
          </div>
        )}

        <p style={{ marginTop: '15px', color: '#666' }}>
          Gap Coverage: {(100 - (skills_gap.gap_percentage || 0)).toFixed(1)}%
        </p>
      </div>

      {/* Recommendations */}
      {recommendations && recommendations.length > 0 && (
        <div className="card">
          <div className="card-title">💬 Recommendations</div>
          <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
            {recommendations.map((rec, idx) => (
              <li
                key={idx}
                style={{
                  padding: '10px',
                  marginBottom: '10px',
                  background: '#f0f2ff',
                  borderLeft: '4px solid #667eea',
                  borderRadius: '4px',
                }}
              >
                {rec}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
