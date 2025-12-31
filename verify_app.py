# Simple test to verify the app can be imported without errors
try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath('.'))
    
    # Import the main function without running the Streamlit app
    from app import main
    print("[OK] App module imports successfully")
    
    # Test a few key functions
    from app import process_uploaded_file, call_ai_model, generate_docx
    print("[OK] Key functions import successfully")
    
    # Test that required libraries are available
    import streamlit as st
    import docx
    import requests
    import google.generativeai
    import fitz
    print("[OK] Required libraries available")
    
    print("\nAll tests passed! The application is ready to run.")
    print("To start the application, run: streamlit run app.py")

except ImportError as e:
    print(f"[ERROR] Import error: {e}")
except Exception as e:
    print(f"[ERROR] Other error: {e}")