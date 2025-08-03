// src/components/Camera.js
import React, { useRef, useState, useEffect } from 'react';

const Camera = ({ onImageCapture }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [hasCamera, setHasCamera] = useState(true);
  const [isCapturing, setIsCapturing] = useState(false);

  useEffect(() => {
    startCamera();
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { 
          facingMode: 'environment', // Use back camera on mobile
          width: { ideal: 1280 },
          height: { ideal: 720 }
        }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      setStream(mediaStream);
    } catch (err) {
      console.error('Error accessing camera:', err);
      setHasCamera(false);
    }
  };

  const captureImage = () => {
    if (!videoRef.current || !canvasRef.current) return;
    
    setIsCapturing(true);
    
    const canvas = canvasRef.current;
    const video = videoRef.current;
    const context = canvas.getContext('2d');
    
    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw video frame to canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convert to blob and pass to parent
    canvas.toBlob((blob) => {
      const file = new File([blob], 'vending-machine.jpg', { type: 'image/jpeg' });
      onImageCapture(file);
      setIsCapturing(false);
    }, 'image/jpeg', 0.8);
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      onImageCapture(file);
    }
  };

  if (!hasCamera) {
    return (
      <div className="camera-fallback">
        <div className="upload-area">
          <h3>📷 Camera not available</h3>
          <p>Upload a photo of the vending machine instead:</p>
          <input
            type="file"
            accept="image/*"
            onChange={handleFileUpload}
            className="file-input"
            id="image-upload"
          />
          <label htmlFor="image-upload" className="upload-button">
            Choose Photo
          </label>
        </div>
      </div>
    );
  }

  return (
    <div className="camera-container">
      <div className="camera-viewport">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="camera-video"
        />
        
        <div className="camera-overlay">
          <div className="scan-frame">
            <div className="corner top-left"></div>
            <div className="corner top-right"></div>
            <div className="corner bottom-left"></div>
            <div className="corner bottom-right"></div>
          </div>
          <p className="scan-instruction">
            Frame the vending machine in the viewfinder
          </p>
        </div>
      </div>
      
      <div className="camera-controls">
        <button
          onClick={captureImage}
          disabled={isCapturing}
          className="capture-button"
        >
          {isCapturing ? '📸 Processing...' : '📸 Scan Snacks'}
        </button>
        
        <input
          type="file"
          accept="image/*"
          onChange={handleFileUpload}
          className="file-input"
          id="backup-upload"
        />
        <label htmlFor="backup-upload" className="upload-link">
          Or upload photo
        </label>
      </div>
      
      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </div>
  );
};

export default Camera;