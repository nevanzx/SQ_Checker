# Survey Questionnaire Quality Checker

This Streamlit application analyzes survey questionnaires using multiple AI models to assess quality metrics. The app allows users to upload survey files, select from various AI models, and receive detailed quality reports in both JSON and DOCX formats.

## Features

- Upload multiple survey questionnaire files (TXT, JSON, CSV, DOCX, PDF)
- Analyze surveys using multiple AI models:
  - DeepSeek Reasoner
  - Gemini 3 Flash
  - Gemini 2.5 Flash
  - OpenRouter (Xiaomi/MIMO)
  - Custom model support
- Model management interface to add and store API keys
- Export analysis results as JSON or DOCX files
- Quality metrics assessment (clarity, bias detection, relevance, etc.)

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:

```bash
streamlit run app.py
```

## Usage

1. Navigate to the "Upload & Analyze" tab
2. Upload one or more survey questionnaire files
3. Select which AI models to use for analysis
4. Click "Analyze Survey Quality" to start the analysis
5. View results in the "Results" tab
6. Download JSON or DOCX reports as needed

## Model Configuration

To use the AI models, you need to provide API keys:

1. Go to the "Model Management" tab
2. Enter your API keys for each model
3. For custom models, add them using the form at the bottom

Supported model providers:
- DeepSeek (requires DeepSeek API key)
- Google Gemini (requires Google API key)
- OpenRouter (requires OpenRouter API key)
- Custom OpenAI-compatible APIs

## File Format Support

The application supports the following file formats:
- TXT - Plain text files
- JSON - Structured data files
- CSV - Comma-separated values
- DOCX - Microsoft Word documents
- PDF - Portable Document Format

## Architecture

The application consists of:
- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `README.md` - This documentation file

The analysis workflow:
1. File upload and processing
2. AI model analysis
3. JSON result generation
4. DOCX report creation