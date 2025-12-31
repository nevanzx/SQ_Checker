"""
Test script for Survey Quality Checker
This script provides a basic test to verify the application components work together
"""
import os
import sys
from pathlib import Path

def test_setup():
    """Test if all required files exist"""
    required_files = [
        "app.py",
        "requirements.txt",
        "README.md"
    ]
    
    print("Testing application setup...")
    for file in required_files:
        if os.path.exists(file):
            print(f"[OK] {file} exists")
        else:
            print(f"[ERROR] {file} missing")
            return False

    print("\nChecking requirements...")
    with open("requirements.txt", "r") as f:
        requirements = f.read()

    required_packages = ["streamlit", "python-docx", "requests", "google-generativeai"]
    for package in required_packages:
        if package in requirements:
            print(f"[OK] {package} in requirements")
        else:
            print(f"[ERROR] {package} missing from requirements")
            return False
    
    print("\nApplication setup is complete!")
    print("\nTo run the application:")
    print("1. Install requirements: pip install -r requirements.txt")
    print("2. Run the app: streamlit run app.py")
    
    return True

if __name__ == "__main__":
    test_setup()