# 🏋️ Exercise-Specific Pose Analysis Guide

This guide shows you how to implement your custom pose analysis code for each exercise.

## 📋 Structure for Each Exercise

Each exercise section in `main.py` follows this pattern:

```python
elif 'exercise_name' in exercise_name_lower:
    # ========== EXERCISE NAME ANALYSIS ==========
    # TODO: Add your exercise-specific code here
    
    # 1. Get landmark positions
    # 2. Calculate specific angles for this exercise
    # 3. Implement rep counting logic
    # 4. Add form feedback
    # 5. Display results on screen
```

## 🎯 Example Implementation: Push-Ups

Here's a complete example for push-ups analysis:

```python
elif 'pushups' in exercise_name_lower:
    # ========== PUSH-UPS ANALYSIS ==========
    
    # Get landmark positions
    left_shoulder = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    left_elbow = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_ELBOW.value]
    left_wrist = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_WRIST.value]
    
    right_shoulder = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    right_elbow = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value]
    right_wrist = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]
    
    left_hip = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_HIP.value]
    left_knee = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
    left_ankle = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
    
    # Calculate angles
    left_arm_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
    right_arm_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
    body_angle = self.calculate_angle(left_shoulder, left_hip, left_ankle)
    
    # Push-up specific logic
    if left_arm_angle < 90 and right_arm_angle < 90:
        # Down position
        cv2.putText(image, "DOWN", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    elif left_arm_angle > 160 and right_arm_angle > 160:
        # Up position
        cv2.putText(image, "UP", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Form feedback
    if body_angle > 170:  # Straight body
        cv2.putText(image, "Good Form!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(image, "Keep body straight", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Display angles
    cv2.putText(image, f"Left Arm: {left_arm_angle:.1f}°", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(image, f"Right Arm: {right_arm_angle:.1f}°", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(image, f"Body: {body_angle:.1f}°", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
```

## 🎯 Example Implementation: Squats

```python
elif 'squats' in exercise_name_lower:
    # ========== SQUATS ANALYSIS ==========
    
    # Get landmark positions
    left_hip = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_HIP.value]
    left_knee = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
    left_ankle = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
    
    right_hip = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
    right_knee = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]
    right_ankle = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]
    
    # Calculate knee angles
    left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
    right_knee_angle = self.calculate_angle(right_hip, right_knee, right_ankle)
    
    # Squat depth analysis
    if left_knee_angle < 90 and right_knee_angle < 90:
        cv2.putText(image, "DEEP SQUAT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    elif left_knee_angle < 120 and right_knee_angle < 120:
        cv2.putText(image, "HALF SQUAT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 165, 0), 2)
    else:
        cv2.putText(image, "STANDING", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Form feedback
    if left_knee_angle < 90 and right_knee_angle < 90:
        cv2.putText(image, "Good Depth!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(image, "Go Deeper", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Display angles
    cv2.putText(image, f"Left Knee: {left_knee_angle:.1f}°", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(image, f"Right Knee: {right_knee_angle:.1f}°", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
```

## 🎯 Example Implementation: Bicep Curls

```python
elif 'barbellcurls' in exercise_name_lower:
    # ========== BARBELL CURLS ANALYSIS ==========
    
    # Get landmark positions
    left_shoulder = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    left_elbow = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_ELBOW.value]
    left_wrist = landmarks_dict[self.mp_pose.PoseLandmark.LEFT_WRIST.value]
    
    right_shoulder = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    right_elbow = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value]
    right_wrist = landmarks_dict[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]
    
    # Calculate arm angles
    left_arm_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
    right_arm_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
    
    # Curl position analysis
    if left_arm_angle < 60 and right_arm_angle < 60:
        cv2.putText(image, "FULL CURL", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    elif left_arm_angle < 90 and right_arm_angle < 90:
        cv2.putText(image, "HALF CURL", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 165, 0), 2)
    else:
        cv2.putText(image, "STARTING POSITION", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Form feedback
    if left_arm_angle < 60 and right_arm_angle < 60:
        cv2.putText(image, "Good Curl!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(image, "Complete the curl", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Display angles
    cv2.putText(image, f"Left Arm: {left_arm_angle:.1f}°", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(image, f"Right Arm: {right_arm_angle:.1f}°", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
```

## 🔧 Available Landmarks

You can access these MediaPipe landmarks:

```python
# Upper body
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16

# Lower body
LEFT_HIP = 23
RIGHT_HIP = 24
LEFT_KNEE = 25
RIGHT_KNEE = 26
LEFT_ANKLE = 27
RIGHT_ANKLE = 28

# Additional landmarks
NOSE = 0
LEFT_EYE = 1
RIGHT_EYE = 2
LEFT_EAR = 7
RIGHT_EAR = 8
```

## 📊 Rep Counting Logic

For rep counting, you can implement state machines:

```python
# Example rep counting for push-ups
class PushUpCounter:
    def __init__(self):
        self.count = 0
        self.stage = None  # 'up' or 'down'
    
    def update(self, arm_angle):
        if arm_angle > 160 and self.stage == 'down':
            self.count += 1
            self.stage = 'up'
        elif arm_angle < 90:
            self.stage = 'down'
        
        return self.count
```

## 🎨 Display Options

You can display information on the video feed:

```python
# Text display
cv2.putText(image, "Text", (x, y), cv2.FONT_HERSHEY_SIMPLEX, size, color, thickness)

# Rectangle
cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

# Circle
cv2.circle(image, (x, y), radius, color, thickness)

# Line
cv2.line(image, (x1, y1), (x2, y2), color, thickness)
```

## 🚀 Implementation Steps

1. **Find your exercise section** in `main.py`
2. **Replace the `pass` statement** with your custom code
3. **Use the landmarks_dict** to get landmark positions
4. **Calculate specific angles** for your exercise
5. **Implement rep counting** if needed
6. **Add form feedback** and display it
7. **Test with your camera**

## 📝 Template for Your Code

```python
elif 'your_exercise' in exercise_name_lower:
    # ========== YOUR EXERCISE ANALYSIS ==========
    
    # 1. Get landmark positions
    landmark1 = landmarks_dict[self.mp_pose.PoseLandmark.LANDMARK_NAME.value]
    landmark2 = landmarks_dict[self.mp_pose.PoseLandmark.LANDMARK_NAME.value]
    landmark3 = landmarks_dict[self.mp_pose.PoseLandmark.LANDMARK_NAME.value]
    
    # 2. Calculate angles
    angle1 = self.calculate_angle(landmark1, landmark2, landmark3)
    angle2 = self.calculate_angle(landmark2, landmark3, landmark1)
    
    # 3. Your exercise-specific logic
    if angle1 < threshold:
        # Do something
        pass
    elif angle1 > threshold:
        # Do something else
        pass
    
    # 4. Form feedback
    if good_form_condition:
        cv2.putText(image, "Good Form!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(image, "Adjust Form", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # 5. Display angles/info
    cv2.putText(image, f"Angle: {angle1:.1f}°", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
```

Now you can paste your specific exercise analysis code in each section!
