from flask import Flask,render_template,request,redirect,session,url_for,Response
from werkzeug.security import generate_password_hash , check_password_hash
from flask_sqlalchemy import SQLAlchemy
import cv2
import mediapipe as mp
import numpy as np
import threading
import time


app=Flask(__name__)
app.secret_key='your_secret_key'

# Configure session settings - use default session type
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

# Configure SQL Alchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)


# Database model Single row with our DB
class User(db.Model):
    # Class Variables
    id=db.Column(db.Integer , primary_key=True)
    username=db.Column(db.String(25),unique=True,nullable=False)
    password_hash=db.Column(db.String(150),nullable=False)

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


# MediaPipe Pose Detection Setup
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
        try:
            # Stop any existing camera first
            self.stop_camera()
            
            # Start new camera
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                self.is_running = True
                # Reset exercise counters for new session
                exercise_counters = [
                    'pullup_counter', 'pullup_stage',
                    'barbellcurls_counter', 'barbellcurls_stage',
                    'pushups_counter', 'pushups_stage',
                    'benchpress_counter', 'benchpress_stage',
                    'dumbbellflyes_counter', 'dumbbellflyes_stage',
                    'overheadpress_counter', 'overheadpress_stage',
                    'lateralraises_counter', 'lateralraises_stage',
                    'frontraises_counter', 'frontraises_stage',
                    'bentoverrows_counter', 'bentoverrows_stage',
                    'latpulldowns_counter', 'latpulldowns_stage',
                    'hammercurls_counter', 'hammercurls_stage',
                    'preachercurls_counter', 'preachercurls_stage',
                    'overheadtricep_counter', 'overheadtricep_stage',
                    'tricepextensions_counter', 'tricepextensions_stage',
                    'closegripbench_counter', 'closegripbench_stage',
                    'squats_counter', 'squats_stage',
                    'deadlifts_counter', 'deadlifts_stage',
                    'lunges_counter', 'lunges_stage'
                ]
                
                for counter_attr in exercise_counters:
                    if counter_attr.endswith('_counter'):
                        setattr(self, counter_attr, 0)
                    elif counter_attr.endswith('_stage'):
                        setattr(self, counter_attr, None)
                
                return True
            else:
                self.is_running = False
                return False
        except Exception as e:
            print(f"Error starting camera: {e}")
            self.is_running = False
            return False
            
    def stop_camera(self):
        """Stop the camera feed"""
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
        # if self.cap is not None and self.cap.isOpened():
        #     self.cap.release()
        #     self.cap = None
        #     cv2.destroyAllWindows()

            # Add a longer delay to ensure camera is properly released
            time.sleep(0.5)
            
    def process_frame(self, frame, exercise_name=None):
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
            
            # Add pose analysis with exercise-specific logic
            self.analyze_pose(results.pose_landmarks, image, exercise_name)
            
        return image
    
    def analyze_pose(self, landmarks, image, exercise_name=None):
        """Analyze pose and provide feedback based on exercise type"""
        # Get landmark positions
        h, w, _ = image.shape
        
        # Get all landmark positions for exercise-specific analysis
        landmarks_dict = {}
        for i, landmark in enumerate(landmarks.landmark):
            landmarks_dict[i] = (landmark.x * w, landmark.y * h)
        left_shoulder = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        left_elbow = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_ELBOW.value]
        left_wrist = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_WRIST.value]
        left_hip = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        left_knee=landmarks_dict[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
        left_ankle=landmarks_dict[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]

                
        right_shoulder = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        right_elbow = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        right_wrist = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]
        right_hip = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        right_knee=landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]
        right_ankle=landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]
                
                # Calculate angles
        left_elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
        left_shoulder_angle = self.calculate_angle(left_hip, left_shoulder, left_elbow)
        right_elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
        right_shoulder_angle = self.calculate_angle(right_hip, right_shoulder, right_elbow)
        right_knee_angle = self.calculate_angle(right_hip, right_knee, right_ankle)
        left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        left_shoulder_angle2 = self.calculate_angle(right_shoulder, left_shoulder, left_elbow)
        right_shoulder_angle2 = self.calculate_angle(left_shoulder, right_shoulder, right_elbow)
        
        # Exercise-specific pose analysis
        if exercise_name:
            exercise_name_lower = exercise_name.lower().replace(' ', '').replace('-', '')
            
            # CHEST EXERCISES
            if 'pushups' in exercise_name_lower:
                # ========== PUSH-UPS ANALYSIS ==========
                # Initialize counter and stage
                if not hasattr(self, 'pushups_counter'):
                    self.pushups_counter = 0
                    self.pushups_stage = None
                

                if (right_elbow_angle <100 and left_elbow_angle <100 and 
                    right_shoulder_angle <45 and left_shoulder_angle <45):
                    self.pushups_stage = "down"
                
                if (right_elbow_angle >150 and left_elbow_angle >150 and 
                    right_shoulder_angle < 45 and left_shoulder_angle < 45 and 
                    self.pushups_stage == 'down'):
                    self.pushups_stage = "up"
                    self.pushups_counter += 1
                
                # Store counter data for API access (no display on camera feed)
                
                pass
                
            elif 'benchpress' in exercise_name_lower:
                # ========== BENCH PRESS ANALYSIS ==========
                # Initialize counter and stage
                if not hasattr(self, 'benchpress_counter'):
                    self.benchpress_counter = 0
                    self.benchpress_stage = None
                
                # TODO: Add your bench press specific code here
                # Example structure:
                # - Calculate arm angles for bench press form
                # - Check shoulder position and stability
                # - Count bench press repetitions
                # - Provide form feedback
                if (right_elbow_angle <100 and left_elbow_angle <100 and 
                    right_shoulder_angle <45 and left_shoulder_angle <45):
                    self.pushups_stage = "down"
                
                if (right_elbow_angle >150 and left_elbow_angle >150 and 
                    right_shoulder_angle < 45 and left_shoulder_angle < 45 and 
                    self.pushups_stage == 'down'):
                    self.pushups_stage = "up"
                    self.pushups_counter += 1

                pass
                
            elif 'dumbbellflyes' in exercise_name_lower:
                # ========== DUMBBELL FLYES ANALYSIS ==========
                # Initialize counter and stage
                if not hasattr(self, 'dumbbellflyes_counter'):
                    self.dumbbellflyes_counter = 0
                    self.dumbbellflyes_stage = None
                # cv2.putText(image, f"L Shoulder: {int(left_shoulder_angle2)}°", 
                #            (int(left_shoulder[0]), int(left_shoulder[1])), 
                #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                # cv2.putText(image, f"R Shoulder: {int(right_shoulder_angle2)}°", 
                #            (int(right_shoulder[0]), int(right_shoulder[1])), 
                #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
                if (right_elbow_angle >140 and left_elbow_angle >140 and 
                    right_shoulder_angle2 >160 and left_shoulder_angle2 >160):
                    self.dumbbellflyes_stage = "down"
                
                if (right_elbow_angle >140 and left_elbow_angle >140 and 
                    right_shoulder_angle2 < 120 and left_shoulder_angle2 < 120 and 
                    self.dumbbellflyes_stage == 'down'):
                    self.dumbbellflyes_stage = "up"
                    self.dumbbellflyes_counter += 1

                pass
                
            # SHOULDER EXERCISES
            elif 'overheadpress' in exercise_name_lower:
                # ========== OVERHEAD PRESS ANALYSIS ==========
                # Initialize counter and stage
                if not hasattr(self, 'overheadpress_counter'):
                    self.overheadpress_counter = 0
                    self.overheadpress_stage = None
                
                # TODO: Add your overhead press specific code here
                # Example structure:
                # - Calculate arm angles for overhead press
                # - Check shoulder stability and core engagement
                # - Count press repetitions
                # - Provide form feedback
                if (right_elbow_angle <30 and left_elbow_angle <30 and 
                    right_shoulder_angle <30 and left_shoulder_angle <30):
                    self.dumbbellflyes_stage = "down"
                
                if (right_elbow_angle >160 and left_elbow_angle >160 and 
                    right_shoulder_angle >160 and left_shoulder_angle >160 and 
                    self.dumbbellflyes_stage == 'down'):
                    self.dumbbellflyes_stage = "up"
                    self.dumbbellflyes_counter += 1
                pass
                
            elif 'lateralraises' in exercise_name_lower:
                # ========== LATERAL RAISES ANALYSIS ==========
                # Initialize counter and stage
                if not hasattr(self, 'lateralraises_counter'):
                    self.lateralraises_counter = 0
                    self.lateralraises_stage = None
                
                # TODO: Add your lateral raises specific code here
                # Example structure:
                # - Calculate arm angles for lateral raise
                # - Check shoulder abduction and form
                # - Count lateral raise repetitions
                # - Provide form feedback
                pass
                
            elif 'frontraises' in exercise_name_lower:
                # ========== FRONT RAISES ANALYSIS ==========
                # Initialize counter and stage
                if not hasattr(self, 'frontraises_counter'):
                    self.frontraises_counter = 0
                    self.frontraises_stage = None
                
                # TODO: Add your front raises specific code here
                # Example structure:
                # - Calculate arm angles for front raise
                # - Check shoulder flexion and form
                # - Count front raise repetitions
                # - Provide form feedback
                pass
                
            # BACK EXERCISES
            elif 'pullup' in exercise_name_lower:
                # ========== PULL-UPS ANALYSIS ==========
                
                # # Get landmark positions
                # left_shoulder = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                # left_elbow = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_ELBOW.value]
                # left_wrist = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_WRIST.value]
                # left_hip = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_HIP.value]
                
                # right_shoulder = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
                # right_elbow = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value]
                # right_wrist = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]
                # right_hip = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
                
                # # Calculate angles
                # left_elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
                # left_shoulder_angle = self.calculate_angle(left_hip, left_shoulder, left_elbow)
                # right_elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
                # right_shoulder_angle = self.calculate_angle(right_hip, right_shoulder, right_elbow)
                
                # Display angles on image
                # cv2.putText(image, f"L Elbow: {int(left_elbow_angle)}°", 
                #            (int(left_elbow[0]), int(left_elbow[1])), 
                #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                # cv2.putText(image, f"L Shoulder: {int(left_shoulder_angle)}°", 
                #            (int(left_shoulder[0]), int(left_shoulder[1])), 
                #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                # cv2.putText(image, f"R Elbow: {int(right_elbow_angle)}°", 
                #            (int(right_elbow[0]), int(right_elbow[1])), 
                #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                # cv2.putText(image, f"R Shoulder: {int(right_shoulder_angle)}°", 
                #            (int(right_shoulder[0]), int(right_shoulder[1])), 
                #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
                # Pull-up rep counting logic
                # Initialize static variables for counter and stage
                if not hasattr(self, 'pullup_counter'):
                    self.pullup_counter = 0
                    self.pullup_stage = None
                
                # Rep counting logic
                if (right_elbow_angle > 160 and left_elbow_angle > 160 and 
                    right_shoulder_angle > 160 and left_shoulder_angle > 160):
                    self.pullup_stage = "down"
                
                if (right_elbow_angle < 30 and left_elbow_angle < 30 and 
                    right_shoulder_angle < 90 and left_shoulder_angle < 90 and 
                    self.pullup_stage == 'down'):
                    self.pullup_stage = "up"
                    self.pullup_counter += 1
                
                # Store counter data for API access (no display on camera feed)
                pass
                
                # # Form feedback
                # if self.pullup_stage == "up":
                #     cv2.putText(image, "Good Pull-up!", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                # elif self.pullup_stage == "down":
                #     cv2.putText(image, "Lower yourself", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                # else:
                #     cv2.putText(image, "Get ready for pull-up", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
            elif 'bentoverrows' in exercise_name_lower:
                # ========== BENT-OVER ROWS ANALYSIS ==========
                # Initialize counter and stage
                if not hasattr(self, 'bentoverrows_counter'):
                    self.bentoverrows_counter = 0
                    self.bentoverrows_stage = None
                
                # TODO: Add your bent-over rows specific code here
                # Example structure:
                # - Calculate arm angles for row movement
                # - Check back angle and core stability
                # - Count row repetitions
                # - Provide form feedback
                pass
                
            elif 'latpulldowns' in exercise_name_lower:
                # ========== LAT PULLDOWNS ANALYSIS ==========
                # Initialize counter and stage
                if not hasattr(self, 'latpulldowns_counter'):
                    self.latpulldowns_counter = 0
                    self.latpulldowns_stage = None
                
                # TODO: Add your lat pulldowns specific code here
                # Example structure:
                # - Calculate arm angles for pulldown movement
                # - Check back engagement and range of motion
                # - Count pulldown repetitions
                # - Provide form feedback
                pass
                
            # BICEP EXERCISES
            elif 'barbellcurls' in exercise_name_lower:
                # ========== BARBELL CURLS ANALYSIS ==========
                # TODO: Add your barbell curls specific code here
                # Example structure:
                # - Calculate arm angles for curl movement
                # - Check bicep engagement and form
                # - Count curl repetitions
                # - Provide form feedback
                
                # left_shoulder = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                # left_elbow = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_ELBOW.value]
                # left_wrist = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_WRIST.value]
                # left_hip = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_HIP.value]
                
                # right_shoulder = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
                # right_elbow = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value]
                # right_wrist = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]
                # right_hip = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_HIP.value]

                # left_elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
                # # left_shoulder_angle = self.calculate_angle(left_hip, left_shoulder, left_elbow)
                # right_elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
                # right_shoulder_angle = self.calculate_angle(right_hip, right_shoulder, right_elbow)

                # Display angles on image
                # cv2.putText(image, f"L Elbow: {int(left_elbow_angle)}°", 
                #            (int(left_elbow[0]), int(left_elbow[1])), 
                #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                # cv2.putText(image, f"L Shoulder: {int(left_shoulder_angle)}°", 
                #            (int(left_shoulder[0]), int(left_shoulder[1])), 
                #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # Initialize static variables for counter and stage
                if not hasattr(self, 'barbellcurls_counter'):
                    self.barbellcurls_counter = 0
                    self.barbellcurls_stage = None

                # Rep counter logic for barbell curls
                if (right_elbow_angle > 160 and left_elbow_angle > 160):
                    self.barbellcurls_stage = "down"
                
                if (right_elbow_angle < 30 and left_elbow_angle < 30 and
                    self.barbellcurls_stage == 'down'):
                    self.barbellcurls_stage = "up"
                    self.barbellcurls_counter += 1
            
                
            elif 'hammercurls' in exercise_name_lower:
                # ========== HAMMER CURLS ANALYSIS ==========
                # Initialize counter and stage
                if not hasattr(self, 'hammercurls_counter'):
                    self.hammercurls_counter = 0
                    self.hammercurls_stage = None
                
                # TODO: Add your hammer curls specific code here
                # Example structure:
                # - Calculate arm angles for hammer curl
                # - Check forearm and bicep engagement
                # - Count hammer curl repetitions
                # - Provide form feedback
                pass
                
            elif 'preachercurls' in exercise_name_lower:
                # ========== PREACHER CURLS ANALYSIS ==========
                # Initialize counter and stage
                if not hasattr(self, 'preachercurls_counter'):
                    self.preachercurls_counter = 0
                    self.preachercurls_stage = None
                
                # TODO: Add your preacher curls specific code here
                # Example structure:
                # - Calculate arm angles for preacher curl
                # - Check isolation and form
                # - Count preacher curl repetitions
                # - Provide form feedback
                pass
                
            # TRICEP EXERCISES
            elif 'overheadtricep' in exercise_name_lower:
                # ========== OVERHEAD TRICEP ANALYSIS ==========
                # Initialize counter and stage
                if not hasattr(self, 'overheadtricep_counter'):
                    self.overheadtricep_counter = 0
                    self.overheadtricep_stage = None
                
                # TODO: Add your overhead tricep specific code here
                # Example structure:
                # - Calculate arm angles for overhead extension
                # - Check tricep engagement and form
                # - Count tricep extension repetitions
                # - Provide form feedback
                pass
                
            elif 'tricepextensions' in exercise_name_lower:
                # ========== TRICEP EXTENSIONS ANALYSIS ==========
                # Initialize counter and stage
                if not hasattr(self, 'tricepextensions_counter'):
                    self.tricepextensions_counter = 0
                    self.tricepextensions_stage = None
                
                # TODO: Add your tricep extensions specific code here
                # Example structure:
                # - Calculate arm angles for tricep extension
                # - Check tricep engagement and form
                # - Count tricep extension repetitions
                # - Provide form feedback
                pass
                
            elif 'closegripbench' in exercise_name_lower:
                # ========== CLOSE-GRIP BENCH PRESS ANALYSIS ==========
                # Initialize counter and stage
                if not hasattr(self, 'closegripbench_counter'):
                    self.closegripbench_counter = 0
                    self.closegripbench_stage = None
                
                # TODO: Add your close-grip bench press specific code here
                # Example structure:
                # - Calculate arm angles for close-grip press
                # - Check tricep engagement and form
                # - Count close-grip press repetitions
                # - Provide form feedback
                pass
                
            # LEG EXERCISES
            elif 'squats' in exercise_name_lower:
                # ========== SQUATS ANALYSIS ==========
                # Initialize counter and stage
                if not hasattr(self, 'squats_counter'):
                    self.squats_counter = 0
                    self.squats_stage = None
                
                # TODO: Add your squats specific code here
                # Example structure:
                # - Calculate knee and hip angles
                # - Check depth and form
                # - Count squat repetitions
                # - Provide form feedback
                pass
                
            elif 'deadlifts' in exercise_name_lower:
                # ========== DEADLIFTS ANALYSIS ==========
                # Initialize counter and stage
                if not hasattr(self, 'deadlifts_counter'):
                    self.deadlifts_counter = 0
                    self.deadlifts_stage = None
                
                # TODO: Add your deadlifts specific code here
                # Example structure:
                # - Calculate hip and back angles
                # - Check form and safety
                # - Count deadlift repetitions
                # - Provide form feedback
                pass
                
            elif 'lunges' in exercise_name_lower:
                # ========== LUNGES ANALYSIS ==========
                # Initialize counter and stage
                if not hasattr(self, 'lunges_counter'):
                    self.lunges_counter = 0
                    self.lunges_stage = None
                
                # TODO: Add your lunges specific code here
                # Example structure:
                # - Calculate knee and hip angles
                # - Check balance and form
                # - Count lunge repetitions
                # - Provide form feedback
                pass
                
            else:
                # Default analysis for unknown exercises
                self.default_pose_analysis(landmarks, image)
        else:
            # Default analysis when no exercise is specified
            self.default_pose_analysis(landmarks, image)
    
    def default_pose_analysis(self, landmarks, image):
        """Default pose analysis for general exercises"""
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
    
    def generate_frames(self, exercise_name=None):
        """Generate camera frames with pose detection"""
        while self.is_running:
            if self.cap is None or not self.cap.isOpened():
                break
                
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Process frame with pose detection and exercise-specific analysis
            processed_frame = self.process_frame(frame, exercise_name)
            
            # Convert to JPEG
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            if not ret:
                continue
                
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Global pose detector instance
pose_detector = PoseDetector()


# Exercise data dictionary
EXERCISES = {
    'chest': [
        {'name': 'Push-ups', 'video': 'static/exercises/push-ups.gif', 'description': 'Classic bodyweight chest exercise'},
        {'name': 'Bench Press', 'video': 'static/exercises/benchpress.gif', 'description': 'Compound chest movement with barbell'},
        {'name': 'Dumbbell Flyes', 'video': 'static/exercises/dumbellflyes.gif', 'description': 'Isolation exercise for chest'}
    ],
    'shoulder': [
        {'name': 'Overhead Press', 'video': 'static/exercises/military-press.gif', 'description': 'Compound shoulder exercise'},
        {'name': 'Dumbbell Lateral Raise', 'video': 'static/exercises/DB_Lateral_raise.gif', 'description': 'Isolation for lateral deltoids'},
        {'name': 'Seated Dumbbell Press', 'video': 'static/exercises/SEAT_DB_SHD_PRESS.gif', 'description': 'Targets anterior deltoids'}
    ],
    'back': [
        {'name': 'Pull-ups', 'video': 'static/exercises/pull-up.gif', 'description': 'Upper body pulling exercise'},
        {'name': 'Bent-over Rows', 'video': 'static/exercises/Barbell-Bent-Over-Row.gif', 'description': 'Compound back exercise'},
        {'name': 'Lat Pulldowns', 'video': 'static/exercises/wide-grip-lat-pulldown.gif', 'description': 'Machine-based back exercise'}
    ],
    'bicep': [
        {'name': 'Barbell Curls', 'video': 'static/exercises/REV_BB_CURL.gif', 'description': 'Classic bicep exercise'},
        {'name': 'Standing Bicep Curls', 'video': 'static/exercises/Alternating-Dumbbell-Curl.gif', 'description': 'Dumbbell bicep variation'},
        {'name': 'Preacher Curls', 'video': 'static/exercises/ez-bar-preacher-curl.gif', 'description': 'Isolation bicep exercise'}
    ],
    'tricep': [
        {'name': 'Overhead Tricep', 'video': 'static/exercises/DB_TRI_EXT.gif', 'description': 'Compound tricep exercise'},
        {'name': 'Tricep Extensions', 'video': 'static/exercises/tricep-extension.gif', 'description': 'Isolation tricep movement'},
        {'name': 'Close-grip Bench Press', 'video': 'static/exercises/Bench-press.gif', 'description': 'Compound tricep exercise'}
    ],
    'legs': [
        {'name': 'Squats', 'video': 'static/exercises/squats.gif', 'description': 'King of leg exercises'},
        {'name': 'Kettlebell Sumo Deadlifts', 'video': 'static/exercises/KB_SM_DL.gif', 'description': 'Posterior chain compound movement'},
        {'name': 'Dumbbell Lying Curl', 'video': 'static/exercises/dumbbell-leg-curl.gif', 'description': 'Unilateral leg exercise'}
    ]
}

# Commented out YouTube video links for reference:
# EXERCISES = {
#     'chest': [
#         {'name': 'Push-ups', 'video': 'https://www.youtube.com/embed/IODxDxX7oi4', 'description': 'Classic bodyweight chest exercise'},
#         {'name': 'Bench Press', 'video': 'https://www.youtube.com/embed/rT7DgCr-3pg', 'description': 'Compound chest movement with barbell'},
#         {'name': 'Dumbbell Flyes', 'video': 'https://www.youtube.com/embed/eozdVDA78K0', 'description': 'Isolation exercise for chest'}
#     ],
#     'shoulder': [
#         {'name': 'Overhead Press', 'video': 'https://www.youtube.com/embed/qEwKJ5Y0J5Q', 'description': 'Compound shoulder exercise'},
#         {'name': 'Lateral Raises', 'video': 'https://www.youtube.com/embed/3VcKaXpzqRo', 'description': 'Isolation for lateral deltoids'},
#         {'name': 'Front Raises', 'video': 'https://www.youtube.com/embed/gzDawZwVHdM', 'description': 'Targets anterior deltoids'}
#     ],
#     'back': [
#         {'name': 'Pull-ups', 'video': 'https://www.youtube.com/embed/eGo4IYlbE5g', 'description': 'Upper body pulling exercise'},
#         {'name': 'Bent-over Rows', 'video': 'https://www.youtube.com/embed/kE6XW2bRwVA', 'description': 'Compound back exercise'},
#         {'name': 'Lat Pulldowns', 'video': 'https://www.youtube.com/embed/CAwf7n6Luuc', 'description': 'Machine-based back exercise'}
#     ],
#     'bicep': [
#         {'name': 'Barbell Curls', 'video': 'https://www.youtube.com/embed/ykJmrZ5v0O4', 'description': 'Classic bicep exercise'},
#         {'name': 'Hammer Curls', 'video': 'https://www.youtube.com/embed/zC3nLlEvin4', 'description': 'Dumbbell bicep variation'},
#         {'name': 'Preacher Curls', 'video': 'https://www.youtube.com/embed/8JtJuihNCpw', 'description': 'Isolation bicep exercise'}
#     ],
#     'tricep': [
#         {'name': 'Dips', 'video': 'https://www.youtube.com/embed/2z8Jgcr-16Q', 'description': 'Compound tricep exercise'},
#         {'name': 'Tricep Extensions', 'video': 'https://www.youtube.com/embed/nRiJVZDpdL0', 'description': 'Isolation tricep movement'},
#         {'name': 'Close-grip Bench Press', 'video': 'https://www.youtube.com/embed/0GQyyCzyx9c', 'description': 'Compound tricep exercise'}
#     ],
#     'legs': [
#         {'name': 'Squats', 'video': 'https://www.youtube.com/embed/YaXPRqUw1Qk', 'description': 'King of leg exercises'},
#         {'name': 'Deadlifts', 'video': 'https://www.youtube.com/embed/1ZXobu7JvvE', 'description': 'Posterior chain compound movement'},
#         {'name': 'Lunges', 'video': 'https://www.youtube.com/embed/3XDriUn0udo', 'description': 'Unilateral leg exercise'}
#     ]
# }


@app.route("/")
def home():
    return render_template("index.html")

# Login Route
@app.route("/login",methods=["POST"])
def login():
    # Collect info from user
    username=request.form['username']
    password=request.form['password']
    redirect_url = request.form.get('redirect_url', url_for('home'))
    user=User.query.filter_by(username=username).first()
    
    if user:
        if user.check_password(password):
            session['username']=username
            session.permanent = True  # Make session permanent
            return redirect(redirect_url)
        else:
            return render_template("index.html", login_error="Incorrect password. Please try again.", username=username)
    else:
        return render_template("index.html", register_error="Invalid username. Please register first.", username=username)

    


# Register Route
@app.route('/register',methods=["POST"])
def register():
    username=request.form['username']
    password=request.form['password']
    redirect_url = request.form.get('redirect_url', url_for('home'))
    user=User.query.filter_by(username=username).first()
    if user:
        return render_template("index.html", register_error="Username already exists. Please try a different username.", username=username)
    else:
        new_user=User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username']=username
        session.permanent = True  # Make session permanent
        return redirect(redirect_url)


# Muscle Groups Route
@app.route("/muscle/<muscle_group>")
def muscle_group(muscle_group):
    if muscle_group not in EXERCISES:
        return redirect(url_for('home'))
    
    return render_template("exercises.html", muscle_group=muscle_group, exercises=EXERCISES[muscle_group])


# Workout Route
@app.route("/workout/<muscle_group>/<exercise_name>")
def workout(muscle_group, exercise_name):
    if muscle_group not in EXERCISES:
        return redirect(url_for('home'))
    
    exercise = None
    for ex in EXERCISES[muscle_group]:
        if ex['name'].lower().replace(' ', '') == exercise_name.lower().replace(' ', ''):
            exercise = ex
            break
    
    if not exercise:
        return redirect(url_for('muscle_group', muscle_group=muscle_group))
    
    return render_template("workout.html", muscle_group=muscle_group, exercise=exercise)


# MediaPipe Camera Routes
@app.route('/video_feed')
def video_feed():
    """Video streaming route for MediaPipe pose detection"""
    # Check if user is logged in
    if 'username' not in session:
        return Response('Unauthorized', status=401)
    
    # Get exercise name from query parameter
    exercise_name = request.args.get('exercise', None)
    return Response(
        pose_detector.generate_frames(exercise_name),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/start_camera')
def start_camera():
    """Start camera route"""
    # Check if user is logged in
    if 'username' not in session:
        return {'status': 'error', 'message': 'Authentication required'}
    
    success = pose_detector.start_camera()
    if success:
        return {'status': 'success', 'message': 'Camera started'}
    else:
        return {'status': 'error', 'message': 'Failed to start camera'}

@app.route('/stop_camera')
def stop_camera():
    """Stop camera route"""
    # Check if user is logged in
    if 'username' not in session:
        return {'status': 'error', 'message': 'Authentication required'}
    
    pose_detector.stop_camera()
    return {'status': 'success', 'message': 'Camera stopped'}

@app.route('/get_counter_data')
def get_counter_data():
    """Get counter data for display on web page"""
    # Check if user is logged in
    if 'username' not in session:
        return {'status': 'error', 'message': 'Authentication required'}
    
    exercise_name = request.args.get('exercise', '').lower().replace(' ', '').replace('-', '')
    
    # Dynamic counter data for all exercises
    exercise_counters = {
        'pullup': ('pullup_counter', 'pullup_stage'),
        'barbellcurls': ('barbellcurls_counter', 'barbellcurls_stage'),
        'pushups': ('pushups_counter', 'pushups_stage'),
        'benchpress': ('benchpress_counter', 'benchpress_stage'),
        'dumbbellflyes': ('dumbbellflyes_counter', 'dumbbellflyes_stage'),
        'overheadpress': ('overheadpress_counter', 'overheadpress_stage'),
        'lateralraises': ('lateralraises_counter', 'lateralraises_stage'),
        'frontraises': ('frontraises_counter', 'frontraises_stage'),
        'bentoverrows': ('bentoverrows_counter', 'bentoverrows_stage'),
        'latpulldowns': ('latpulldowns_counter', 'latpulldowns_stage'),
        'hammercurls': ('hammercurls_counter', 'hammercurls_stage'),
        'preachercurls': ('preachercurls_counter', 'preachercurls_stage'),
        'overheadtricep': ('overheadtricep_counter', 'overheadtricep_stage'),
        'tricepextensions': ('tricepextensions_counter', 'tricepextensions_stage'),
        'closegripbench': ('closegripbench_counter', 'closegripbench_stage'),
        'squats': ('squats_counter', 'squats_stage'),
        'deadlifts': ('deadlifts_counter', 'deadlifts_stage'),
        'lunges': ('lunges_counter', 'lunges_stage')
    }
    
    # Find matching exercise
    for exercise_key, (counter_attr, stage_attr) in exercise_counters.items():
        if exercise_key in exercise_name:
            if hasattr(pose_detector, counter_attr):
                return {
                    'status': 'success',
                    'counter': getattr(pose_detector, counter_attr),
                    'position': getattr(pose_detector, stage_attr) if getattr(pose_detector, stage_attr) else "None"
                }
            else:
                # Return default values if counter not initialized
                return {
                    'status': 'success',
                    'counter': 0,
                    'position': "None"
                }
    
    # Default response for unknown exercises
    return {
        'status': 'success',
        'counter': 0,
        'position': "None"
    }


# Logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

     

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)



