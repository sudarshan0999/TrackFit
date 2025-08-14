import cv2
import numpy as np
import mediapipe as mp

# Function to calculate the angle between 3 points
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle
        
    return angle

# MediaPipe setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize counters and stages
counter_left = 0
stage_left = None

counter_right = 0
stage_right = None

# Start capturing video
cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR for OpenCV
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            
            # LEFT ARM
            shoulder_l = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow_l = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist_l = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            hip_l = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

            angle_elbow_l = calculate_angle(shoulder_l, elbow_l, wrist_l)
            angle_shoulder_l = calculate_angle(hip_l,shoulder_l, elbow_l)
            

            # Display angle at elbow
            cv2.putText(image, str(int(angle_elbow_l)),
                        tuple(np.multiply(elbow_l, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            #Display angle at shoulder
            cv2.putText(image, str(int(angle_shoulder_l)),
                        tuple(np.multiply(shoulder_l, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            # Rep counter logic - LEFT
            # if angle_l > 160:
            #     stage_left = "down"
            # if angle_l < 45 and stage_left == 'down':
            #     stage_left = "up"
            #     counter_left += 1

            # RIGHT ARM
            shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist_r = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            hip_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

            angle_elbow_r = calculate_angle(shoulder_r, elbow_r, wrist_r)
            angle_shoulder_r = calculate_angle(hip_r,shoulder_r, elbow_r)

            # Display angle at elbow
            cv2.putText(image, str(int(angle_elbow_r)),
                        tuple(np.multiply(elbow_r, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            #Display angle at shoulder
            cv2.putText(image, str(int(angle_shoulder_r)),
                        tuple(np.multiply(shoulder_r, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            # Rep counter logic - RIGHT
            if angle_elbow_r > 160 and angle_elbow_l >160 and angle_shoulder_r >160 and angle_shoulder_l > 160 :
                stage_right = "down"
            if angle_elbow_r < 30 and angle_elbow_l <30 and angle_shoulder_r <90 and angle_shoulder_l <90 and stage_right == 'down':
                stage_right = "up"
                counter_right += 1

        except:
            pass

        # Render left counter box
        cv2.rectangle(image, (0, 0), (100,80), (255, 216, 173), -1)
        cv2.putText(image, 'Count', (22, 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, str(counter_right), (30, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3, cv2.LINE_AA)
        
        # Render up-down counter box
        cv2.rectangle(image, (500, 0), (610,80), (255, 216, 173), -1)
        cv2.putText(image, 'Position', (510, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, str(stage_right), (510, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3, cv2.LINE_AA)

        # Render right counter box
        # cv2.rectangle(image, (440, 0), (610, 70), (0, 0, 255), -1)
        # # cv2.putText(image, 'RIGHT', (450, 20),
        # #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)
        # cv2.putText(image, str(counter_left), (470, 60),
        #             cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)

        # Draw landmarks
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        )

        # Display image
        cv2.imshow('Bicep Curl Tracker', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Cleanup
cap.release()
cv2.destroyAllWindows()
