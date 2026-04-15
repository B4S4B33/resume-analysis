import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

export default function FileUploader({ onFileSelect, disabled = false, label = null }) {
  const [fileName, setFileName] = useState(null);
  const [error, setError] = useState(null);

  const onDrop = useCallback(
    (acceptedFiles) => {
      setError(null);

      if (acceptedFiles.length === 0) {
        setError('Invalid file format. Please upload .txt, .pdf, or .docx');
        return;
      }

      const file = acceptedFiles[0];
      const validExtensions = ['.txt', '.pdf', '.docx'];
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

      if (!validExtensions.includes(fileExtension)) {
        setError('Invalid file format. Please upload .txt, .pdf, or .docx');
        return;
      }

      if (file.size > 10 * 1024 * 1024) {
        setError('File is too large. Maximum size is 10MB');
        return;
      }

      setFileName(file.name);
      onFileSelect(file);
    },
    [onFileSelect]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.txt'],
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    disabled,
    multiple: false,
  });

  const defaultLabel = label || 'resume';

  return (
    <div>
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'active' : ''}`}
        style={{ opacity: disabled ? 0.6 : 1, pointerEvents: disabled ? 'none' : 'auto' }}
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>📂 Drop the file here...</p>
        ) : (
          <div>
            <p>📄 Drag and drop your {defaultLabel} file here</p>
            <p style={{ fontSize: '0.9em', color: '#999' }}>
              or click to select (Supported: .txt, .pdf, .docx)
            </p>
          </div>
        )}
      </div>
      {fileName && (
        <p style={{ marginTop: '10px', color: '#28a745', fontWeight: 600 }}>
          ✓ File selected: {fileName}
        </p>
      )}
      {error && (
        <div className="alert alert-error" style={{ marginTop: '10px' }}>
          {error}
        </div>
      )}
    </div>
  );
}
