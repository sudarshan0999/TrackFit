# 🚀 Setup Guide - FormAI Fitness App

## 📋 Prerequisites

- Python 3.8 or higher
- Webcam for pose detection
- Modern web browser

## 🔧 Virtual Environment Setup

### **Windows (PowerShell/Command Prompt)**

1. **Navigate to your project directory**
   ```bash
   cd "C:\Users\sudar\OneDrive\Desktop\Pose Detection\login2"
   ```

2. **Activate the virtual environment**
   ```bash
   # If using PowerShell
   .\.venv\Scripts\Activate.ps1
   
   # If using Command Prompt
   .\.venv\Scripts\activate.bat
   ```

3. **Verify activation**
   ```bash
   # You should see (.venv) at the beginning of your command prompt
   (.venv) C:\Users\sudar\OneDrive\Desktop\Pose Detection\login2>
   ```

### **macOS/Linux (Terminal)**

1. **Navigate to your project directory**
   ```bash
   cd /path/to/your/login2
   ```

2. **Activate the virtual environment**
   ```bash
   source .venv/bin/activate
   ```

3. **Verify activation**
   ```bash
   # You should see (.venv) at the beginning of your terminal prompt
   (.venv) username@computer:~/login2$
   ```

## 📦 Install Dependencies

Once your virtual environment is activated:

```bash
pip install -r requirements.txt
```

## 🎬 GIF Setup Instructions

### **1. Create Exercise GIFs Directory**

Create the following folder structure in your `static` folder:

```
static/
├── exercises/
│   ├── chest/
│   │   ├── pushups.gif
│   │   ├── benchpress.gif
│   │   └── dumbbellflyes.gif
│   ├── shoulder/
│   │   ├── overheadpress.gif
│   │   ├── lateralraises.gif
│   │   └── frontraises.gif
│   ├── back/
│   │   ├── pullups.gif
│   │   ├── bentoverrows.gif
│   │   └── latpulldowns.gif
│   ├── bicep/
│   │   ├── barbellcurls.gif
│   │   ├── hammercurls.gif
│   │   └── preachercurls.gif
│   ├── tricep/
│   │   ├── dips.gif
│   │   ├── tricepextensions.gif
│   │   └── closegripbench.gif
│   └── legs/
│       ├── squats.gif
│       ├── deadlifts.gif
│       └── lunges.gif
```

### **2. GIF Requirements**

- **Format**: GIF (animated)
- **Size**: Recommended 400x300 pixels or similar aspect ratio
- **Duration**: 3-5 seconds loop
- **Quality**: Clear, well-lit exercise demonstrations
- **File Size**: Keep under 2MB for fast loading

### **3. GIF Sources**

You can create GIFs from:
- **YouTube videos**: Use online tools like GIPHY, EZGIF, or Kapwing
- **Stock footage**: Purchase from sites like Shutterstock or iStock
- **Record your own**: Use screen recording software
- **Free resources**: Find exercise GIFs on GIPHY or similar platforms

### **4. Naming Convention**

Use the exact filenames specified in the code:
- `pushups.gif`
- `benchpress.gif`
- `dumbbellflyes.gif`
- `overheadpress.gif`
- `lateralraises.gif`
- `frontraises.gif`
- `pullups.gif`
- `bentoverrows.gif`
- `latpulldowns.gif`
- `barbellcurls.gif`
- `hammercurls.gif`
- `preachercurls.gif`
- `dips.gif`
- `tricepextensions.gif`
- `closegripbench.gif`
- `squats.gif`
- `deadlifts.gif`
- `lunges.gif`

## 🚀 Running the Application

### **1. Activate Virtual Environment**
```bash
# Windows
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Run the Application**
```bash
python main.py
```

### **4. Open Browser**
Navigate to `http://localhost:5000`

## 🔍 Troubleshooting

### **Virtual Environment Issues**

**Problem**: "Activate.ps1 cannot be loaded because running scripts is disabled"
```bash
# Solution: Run PowerShell as Administrator and execute:
Set-ExecutionPolicy RemoteSigned
```

**Problem**: "No module named 'flask'"
```bash
# Solution: Make sure virtual environment is activated, then:
pip install -r requirements.txt
```

**Problem**: "Virtual environment not found"
```bash
# Solution: Create a new virtual environment:
python -m venv .venv
```

### **GIF Issues**

**Problem**: GIFs not displaying
- Check file paths are correct
- Ensure GIF files exist in `static/exercises/` folder
- Verify file permissions

**Problem**: GIFs too large/slow
- Compress GIFs using online tools
- Reduce frame rate or duration
- Optimize file size

### **Camera Issues**

**Problem**: Camera not working
```bash
# Check if OpenCV can access camera:
python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"
```

**Problem**: MediaPipe errors
```bash
# Update MediaPipe:
pip install --upgrade mediapipe
```

## 📁 File Structure

```
login2/
├── .venv/                    # Virtual environment
├── static/
│   ├── exercises/            # GIF files here
│   │   ├── pushups.gif
│   │   ├── benchpress.gif
│   │   └── ...
│   ├── background.jpg
│   ├── logo.png
│   └── ...
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── exercises.html
│   └── workout.html
├── main.py                   # Main application
├── requirements.txt          # Dependencies
├── README.md                # Project documentation
├── SETUP_GUIDE.md           # This file
└── mediapipe_integration.py # MediaPipe example
```

## 🎯 Quick Start Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] GIF files placed in `static/exercises/` folder
- [ ] Application running (`python main.py`)
- [ ] Browser opened to `http://localhost:5000`
- [ ] Camera permissions granted
- [ ] MediaPipe pose detection working

## 🔧 Development Tips

### **Adding New Exercises**
1. Add GIF to `static/exercises/` folder
2. Update `EXERCISES` dictionary in `main.py`
3. Restart application

### **Modifying Pose Analysis**
1. Edit `analyze_pose` method in `PoseDetector` class
2. Add exercise-specific angle calculations
3. Test with camera feed

### **Customizing Styling**
1. Edit CSS in template files
2. Modify Bootstrap classes
3. Update color schemes

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Ensure virtual environment is activated
4. Check file paths and permissions
5. Review browser console for errors
