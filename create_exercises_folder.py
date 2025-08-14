#!/usr/bin/env python3
"""
Script to create the exercises folder structure for GIF files
"""

import os
import sys

def create_exercises_structure():
    """Create the exercises folder structure"""
    
    # Base directory
    base_dir = "static/exercises"
    
    # Exercise categories and their GIF files
    exercises = {
        'chest': ['pushups.gif', 'benchpress.gif', 'dumbbellflyes.gif'],
        'shoulder': ['overheadpress.gif', 'lateralraises.gif', 'frontraises.gif'],
        'back': ['pullups.gif', 'bentoverrows.gif', 'latpulldowns.gif'],
        'bicep': ['barbellcurls.gif', 'hammercurls.gif', 'preachercurls.gif'],
        'tricep': ['dips.gif', 'tricepextensions.gif', 'closegripbench.gif'],
        'legs': ['squats.gif', 'deadlifts.gif', 'lunges.gif']
    }
    
    try:
        # Create base directory
        os.makedirs(base_dir, exist_ok=True)
        print(f"✅ Created directory: {base_dir}")
        
        # Create subdirectories and placeholder files
        for category, gif_files in exercises.items():
            category_dir = os.path.join(base_dir, category)
            os.makedirs(category_dir, exist_ok=True)
            print(f"✅ Created directory: {category_dir}")
            
            # Create placeholder files
            for gif_file in gif_files:
                file_path = os.path.join(category_dir, gif_file)
                if not os.path.exists(file_path):
                    # Create a placeholder file
                    with open(file_path, 'w') as f:
                        f.write("# Placeholder for " + gif_file + "\n")
                        f.write("# Replace this file with your actual GIF\n")
                    print(f"📁 Created placeholder: {file_path}")
                else:
                    print(f"⚠️  File already exists: {file_path}")
        
        print("\n🎉 Exercise folder structure created successfully!")
        print("\n📋 Next steps:")
        print("1. Replace placeholder files with your actual GIF files")
        print("2. Ensure GIF files are properly named")
        print("3. Keep file sizes under 2MB for optimal performance")
        print("4. Test the application with: python main.py")
        
    except Exception as e:
        print(f"❌ Error creating folder structure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Creating exercise folder structure...")
    create_exercises_structure()
