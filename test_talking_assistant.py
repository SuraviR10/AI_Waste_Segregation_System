"""
Test script for Talking Earth Assistant
Run this to verify the assistant is working correctly
"""

import sys
from pathlib import Path

def check_files():
    """Check if all required files exist"""
    print("Checking Talking Assistant Setup...\n")
    
    required_files = {
        'talking_assistant.py': 'Talking Assistant Module',
        'earth_mascot.py': 'Earth Mascot Module',
        'earth_dialogues.py': 'Earth Dialogues Module',
        'app.py': 'Main Application'
    }
    
    image_files = {
        'images/earth_sad.jpg': 'Sad Earth Image',
        'images/earth_happy.jpg': 'Happy Earth Image',
        'images/earth_thinking.jpg': 'Thinking Earth Image'
    }
    
    all_good = True
    
    # Check Python files
    print("Python Files:")
    for file, desc in required_files.items():
        if Path(file).exists():
            print(f"  [OK] {desc}: {file}")
        else:
            print(f"  [MISSING] {desc}: {file}")
            all_good = False
    
    print("\nEarth Character Images:")
    for file, desc in image_files.items():
        if Path(file).exists():
            print(f"  [OK] {desc}: {file}")
        else:
            print(f"  [WARNING] {desc}: {file} - NOT FOUND (will use emoji fallback)")
    
    print("\n" + "="*60)
    
    if all_good:
        print("[OK] All required files are present!")
        print("\nYour Talking Assistant is ready!")
        print("\nNext Steps:")
        print("   1. Add Earth character images to images/ folder")
        print("   2. Run: streamlit run app.py")
        print("   3. Navigate to 'Scan Waste' page")
        print("   4. Watch Earth talk!")
    else:
        print("[ERROR] Some required files are missing!")
        print("\nPlease ensure all files are in place.")
    
    print("="*60)
    
    return all_good

def test_imports():
    """Test if modules can be imported"""
    print("\nTesting Module Imports...\n")
    
    try:
        from talking_assistant import show_talking_assistant, show_quick_reaction
        print("  [OK] talking_assistant module imported successfully")
    except Exception as e:
        print(f"  [ERROR] Error importing talking_assistant: {e}")
        return False
    
    try:
        from earth_mascot import show_earth_mascot, get_earth_message
        print("  [OK] earth_mascot module imported successfully")
    except Exception as e:
        print(f"  [ERROR] Error importing earth_mascot: {e}")
        return False
    
    try:
        from earth_dialogues import EARTH_DIALOGUES, EARTH_STORY
        print("  [OK] earth_dialogues module imported successfully")
    except Exception as e:
        print(f"  [ERROR] Error importing earth_dialogues: {e}")
        return False
    
    print("\n[OK] All modules imported successfully!")
    return True

def show_features():
    """Display feature information"""
    print("\nTalking Assistant Features:\n")
    
    features = [
        "Animated Earth character with mouth movements",
        "Speech bubbles with dynamic messages",
        "Sound wave animations",
        "3 different moods (happy, sad, thinking)",
        "Timed display (2-4 seconds)",
        "Smooth floating animations",
        "Responsive design",
        "Automatic fallback to emojis"
    ]
    
    for feature in features:
        print(f"  - {feature}")
    
    print("\nWhen Earth Talks:")
    scenarios = [
        "Welcome message (first visit)",
        "Analyzing waste (during detection)",
        "Success celebration (correct classification)",
        "Streak celebration (3+ correct)",
        "Environmental awareness (education page)"
    ]
    
    for scenario in scenarios:
        print(f"  - {scenario}")

def main():
    print("\n" + "="*60)
    print("TALKING EARTH ASSISTANT - SETUP VERIFICATION")
    print("="*60 + "\n")
    
    # Check files
    files_ok = check_files()
    
    if files_ok:
        # Test imports
        imports_ok = test_imports()
        
        if imports_ok:
            # Show features
            show_features()
            
            print("\n" + "="*60)
            print("READY TO LAUNCH!")
            print("="*60)
            print("\nRun: streamlit run app.py")
            print("\nRead: TALKING_ASSISTANT_GUIDE.md for full documentation")
            print("\n")
    else:
        print("\nPlease fix the issues above before running the app.")

if __name__ == "__main__":
    main()
