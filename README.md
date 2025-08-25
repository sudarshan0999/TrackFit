# VisionFit - Fitness Pose Detection App

A comprehensive fitness application with MediaPipe pose detection for real-time exercise form analysis.

## 🚀 Features

- **Multi-level Navigation**: Muscle groups → Exercises → Workout interface
<!-- - **Real YouTube Videos**: Each exercise has its own instructional video -->
- **MediaPipe Integration**: Real-time pose detection and form analysis
- **User Authentication**: Login/Register system with SQLite database
- **Responsive Design**: Modern UI with Bootstrap and custom styling

## 📋 Prerequisites

- Python 3.8 or higher
- Webcam for pose detection
- Modern web browser

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd login2
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## 🎯 How to Use

### 1. Navigation Flow
1. **Home Page**: Select a muscle group (Chest, Shoulder, Back, Biceps, Triceps, Legs)
2. **Exercise Page**: Choose from 3 exercises for that muscle group
3. **Workout Page**: Watch video on left, use camera on right

### 2. Video Integration
<!-- - Each exercise has a real YouTube video -->
<!-- - Videos are embedded with autoplay controls -->
<!-- - Play, Pause, and Restart functionality -->
- Each exercise has a GIF showing how to do that workout

### 3. MediaPipe Pose Detection

#### Starting the Camera
1. Click "Start Camera" button
2. Allow camera permissions in your browser
3. The camera feed will appear with pose landmarks

#### ML Model Features
- **Real-time Pose Detection**: 33 body landmarks
- **Angle Calculations**: Arm angles for form analysis
<!-- - **Form Feedback**: Visual indicators for good/bad form -->
- **Live Analysis**: Continuous monitoring during exercise

#### Pose Analysis Details
The ML model analyzes:
- **Arm Angles**: Left and right arm angles in degrees
- **Form Quality**: Green "Good Form!" or red "Adjust Form"
- **Landmark Tracking**: Real-time body point detection

## 🔧 MediaPipe Integration Guide

### Core Components

#### 1. PoseDetector Class
```python
class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
```

#### 2. Frame Processing
```python
def process_frame(self, frame):
    # Convert BGR to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process with MediaPipe
    results = self.pose.process(image)
    
    # Draw landmarks
    if results.pose_landmarks:
        self.mp_drawing.draw_landmarks(
            image, 
            results.pose_landmarks, 
            self.mp_pose.POSE_CONNECTIONS
        )
```

#### 3. Pose Analysis
```python
def analyze_pose(self, landmarks, image):
    # Get shoulder, elbow, wrist positions
    left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
    left_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW]
    left_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
    
    # Calculate angles
    left_arm_angle = self.calculate_angle(
        [left_shoulder.x * w, left_shoulder.y * h],
        [left_elbow.x * w, left_elbow.y * h],
        [left_wrist.x * w, left_wrist.y * h]
    )
```

### API Endpoints

#### Camera Control
- `GET /start_camera`: Start camera feed
- `GET /stop_camera`: Stop camera feed
- `GET /video_feed`: Stream camera with pose detection

#### Exercise Routes
- `GET /muscle/<muscle_group>`: Show exercises for muscle group
- `GET /workout/<muscle_group>/<exercise_name>`: Workout interface

<!-- ## 📊 Exercise Database

### Chest Exercises
- **Push-ups**: `https://www.youtube.com/embed/IODxDxX7oi4`
- **Bench Press**: `https://www.youtube.com/embed/rT7DgCr-3pg`
- **Dumbbell Flyes**: `https://www.youtube.com/embed/eozdVDA78K0`

### Shoulder Exercises
- **Overhead Press**: `https://www.youtube.com/embed/qEwKJ5Y0J5Q`
- **Lateral Raises**: `https://www.youtube.com/embed/3VcKaXpzqRo`
- **Front Raises**: `https://www.youtube.com/embed/gzDawZwVHdM`

### Back Exercises
- **Pull-ups**: `https://www.youtube.com/embed/eGo4IYlbE5g`
- **Bent-over Rows**: `https://www.youtube.com/embed/kE6XW2bRwVA`
- **Lat Pulldowns**: `https://www.youtube.com/embed/CAwf7n6Luuc`

### Bicep Exercises
- **Barbell Curls**: `https://www.youtube.com/embed/ykJmrZ5v0O4`
- **Hammer Curls**: `https://www.youtube.com/embed/zC3nLlEvin4`
- **Preacher Curls**: `https://www.youtube.com/embed/8JtJuihNCpw`

### Tricep Exercises
- **Dips**: `https://www.youtube.com/embed/2z8Jgcr-16Q`
- **Tricep Extensions**: `https://www.youtube.com/embed/nRiJVZDpdL0`
- **Close-grip Bench Press**: `https://www.youtube.com/embed/0GQyyCzyx9c`

### Leg Exercises
- **Squats**: `https://www.youtube.com/embed/YaXPRqUw1Qk`
- **Deadlifts**: `https://www.youtube.com/embed/1ZXobu7JvvE`
- **Lunges**: `https://www.youtube.com/embed/3XDriUn0udo`

## 🎨 Customization

### Adding New Exercises
1. Update the `EXERCISES` dictionary in `main.py`
2. Add video URL and description
3. The system will automatically create navigation

### Modifying Pose Analysis
1. Edit the `analyze_pose` method in `PoseDetector` class
2. Add new angle calculations for different exercises
3. Customize form feedback logic

### Styling Changes
- Edit CSS in template files
- Modify Bootstrap classes
- Update color schemes and animations

## 🔍 Troubleshooting

### Camera Issues
- Ensure camera permissions are granted
- Check if camera is being used by another application
- Try different camera index (0, 1, 2) in `cv2.VideoCapture()`

### MediaPipe Issues
- Update MediaPipe: `pip install --upgrade mediapipe`
- Check OpenCV version compatibility
- Ensure sufficient lighting for pose detection

### Performance Issues
- Reduce frame resolution in `cv2.VideoCapture()`
- Lower MediaPipe confidence thresholds
- Close other applications using camera

## 📱 Browser Compatibility

- **Chrome**: Full support
- **Firefox**: Full support
- **Safari**: Limited camera support
- **Edge**: Full support

## 🔒 Security Notes

- Camera access requires HTTPS in production
- User data is stored locally in SQLite
- No external API calls for sensitive data

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production (with Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "main.py"]
```

## 📈 Future Enhancements

- [ ] Exercise-specific pose analysis
- [ ] Rep counting and tracking
- [ ] Progress tracking and statistics
- [ ] Mobile app version
- [ ] Social features and sharing
- [ ] AI-powered exercise recommendations -->

<!-- ## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. -->

<!-- ## 🙏 Acknowledgments

- MediaPipe team for pose detection
- GIF for exercise 
- Bootstrap for UI components
- Flask community for web framework -->
