import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, render_template, Response
import threading
import time

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.cap = None
        self.is_running = False
        
    def start_camera(self):
        """Start the camera feed"""
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            self.is_running = True
            
    def stop_camera(self):
        """Stop the camera feed"""
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            
    def process_frame(self, frame):
        """Process a single frame with MediaPipe pose detection"""
        # Convert BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the image
        results = self.pose.process(image)
        
        # Convert back to BGR for OpenCV
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Draw pose landmarks
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                image, 
                results.pose_landmarks, 
                self.mp_pose.POSE_CONNECTIONS
            )
            
            # Add pose analysis
            self.analyze_pose(results.pose_landmarks, image)
            
        return image
    
    def analyze_pose(self, landmarks, image):
        """Analyze pose and provide feedback"""
        # Get landmark positions
        h, w, _ = image.shape
        
        # Example: Check if arms are raised (for shoulder exercises)
        left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW]
        left_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
        
        right_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
        right_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]
        
        # Calculate arm angles
        left_arm_angle = self.calculate_angle(
            [left_shoulder.x * w, left_shoulder.y * h],
            [left_elbow.x * w, left_elbow.y * h],
            [left_wrist.x * w, left_wrist.y * h]
        )
        
        right_arm_angle = self.calculate_angle(
            [right_shoulder.x * w, right_shoulder.y * h],
            [right_elbow.x * w, right_elbow.y * h],
            [right_wrist.x * w, right_wrist.y * h]
        )
        
        # Add feedback text
        feedback = f"Left Arm: {left_arm_angle:.1f}° | Right Arm: {right_arm_angle:.1f}°"
        cv2.putText(image, feedback, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Add form feedback
        if left_arm_angle > 150 and right_arm_angle > 150:
            cv2.putText(image, "Good Form!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(image, "Adjust Form", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    def calculate_angle(self, a, b, c):
        """Calculate angle between three points"""
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
            
        return angle
    
    def generate_frames(self):
        """Generate camera frames with pose detection"""
        while self.is_running:
            if self.cap is None or not self.cap.isOpened():
                break
                
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Process frame with pose detection
            processed_frame = self.process_frame(frame)
            
            # Convert to JPEG
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            if not ret:
                continue
                
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Global pose detector instance
pose_detector = PoseDetector()

def create_app():
    """Create Flask app with MediaPipe integration"""
    app = Flask(__name__)
    
    @app.route('/video_feed')
    def video_feed():
        """Video streaming route"""
        return Response(
            pose_detector.generate_frames(),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )
    
    @app.route('/start_camera')
    def start_camera():
        """Start camera route"""
        pose_detector.start_camera()
        return {'status': 'success', 'message': 'Camera started'}
    
    @app.route('/stop_camera')
    def stop_camera():
        """Stop camera route"""
        pose_detector.stop_camera()
        return {'status': 'success', 'message': 'Camera stopped'}
    
    return app

# Usage in your main.py:
"""
# Add these imports to your main.py
from mediapipe_integration import pose_detector

# Add these routes to your main.py
@app.route('/video_feed')
def video_feed():
    return Response(
        pose_detector.generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/start_camera')
def start_camera():
    pose_detector.start_camera()
    return {'status': 'success', 'message': 'Camera started'}

@app.route('/stop_camera')
def stop_camera():
    pose_detector.stop_camera()
    return {'status': 'success', 'message': 'Camera stopped'}
"""
