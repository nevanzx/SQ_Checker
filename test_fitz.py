try:
    import fitz
    print("fitz module is available")
    print("PyMuPDF version:", fitz.__version__)
except ImportError as e:
    print(f"ImportError: {e}")
    print("fitz module is not available")
    
# Also test importing other modules to make sure the environment is set up correctly
modules_to_test = [
    'streamlit',
    'docx',
    'requests',
    'openai',
    'google.generativeai',
    'pydantic',
    'fitz'
]

for module in modules_to_test:
    try:
        __import__(module)
        print(f"✓ {module} is available")
    except ImportError as e:
        print(f"✗ {module} is NOT available - {e}")