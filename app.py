import streamlit as st
import os
import json
import tempfile
from docx import Document
from docx.shared import Inches
from datetime import datetime
import requests
import time

# Import the prompts module
from prompts import (
    get_deepseek_prompt,
    get_gemini_prompt,
    get_openrouter_prompt,
    get_generic_prompt
)

# Function to load API keys from key.json
def load_api_keys():
    try:
        with open('key.json', 'r') as f:
            keys_data = json.load(f)

        # Create a mapping from service names to API keys
        key_map = {}
        for service in keys_data.get('apis', []):
            name = service['name']
            keys = service['keys']
            # Use the first key if multiple keys are provided
            key_map[name] = keys[0] if keys else ""

        return key_map
    except FileNotFoundError:
        # If key.json doesn't exist, return an empty mapping
        return {}
    except Exception as e:
        st.error(f"Error loading API keys: {e}")
        return {}

def main():
    # Load API keys from key.json
    api_keys = load_api_keys()

    # Initialize session state
    if 'models' not in st.session_state:
        st.session_state.models = [
            {"name": "DeepSeek Reasoner", "api_key": api_keys.get('deepseek', ''), "provider": "deepseek", "temperature": 0.3},
            {"name": "Gemini 3 Flash", "api_key": api_keys.get('gemini', ''), "provider": "gemini3", "temperature": 0.3},
            {"name": "Gemini 2.5 Flash", "api_key": api_keys.get('gemini', ''), "provider": "gemini25", "temperature": 0.3},
            {"name": "OpenRouter (MIMO)", "api_key": api_keys.get('openrounter', ''), "provider": "openrouter", "temperature": 0.3}
        ]

    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []

    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = []

    st.set_page_config(
        page_title="Survey Questionnaire Quality Checker",
        page_icon="📋",
        layout="wide"
    )

    st.title("📋 Survey Questionnaire Quality Checker")
    st.markdown("""
    This application analyzes survey questionnaires using multiple AI models to assess quality metrics.
    Upload your survey files, select AI models, and get detailed quality reports.
    """)

    # Create tabs for different sections - removed Model Management tab
    tab1, tab2 = st.tabs(["Upload & Results", "Settings"])

    with tab1:
        upload_and_results_section()

    with tab2:
        settings_section()

def upload_and_results_section():
    # API key upload section (at the top)
    st.subheader("Upload API Keys File")
    uploaded_key_file = st.file_uploader(
        "Upload key.json file to update all API keys",
        type=['json'],
        key="key_file_uploader_combined"
    )

    if uploaded_key_file is not None:
        try:
            # Load the uploaded JSON file
            uploaded_keys = json.load(uploaded_key_file)

            # Validate the structure of the uploaded file
            if 'apis' not in uploaded_keys:
                st.error("Uploaded file is not a valid key.json format. Missing 'apis' key.")
            else:
                # Update the session state models with the uploaded keys
                for service in uploaded_keys['apis']:
                    service_name = service['name']
                    service_keys = service['keys']

                    # Update the corresponding model in session state
                    for model in st.session_state.models:
                        if service_name == 'deepseek' and model['provider'] == 'deepseek':
                            model['api_key'] = service_keys[0] if service_keys else ""
                        elif service_name == 'gemini' and model['provider'] in ['gemini3', 'gemini25']:
                            model['api_key'] = service_keys[0] if service_keys else ""
                        elif service_name == 'openrounter' and model['provider'] == 'openrouter':
                            model['api_key'] = service_keys[0] if service_keys else ""

                # Save the uploaded keys to the local key.json file
                with open('key.json', 'w') as f:
                    json.dump(uploaded_keys, f, indent=2)

                st.success("API keys updated successfully from uploaded file!")
                # Removed st.rerun() to prevent the file uploader from flashing
                # The API keys are updated in session state and will be used in subsequent calls
        except json.JSONDecodeError:
            st.error("Uploaded file is not a valid JSON file.")
        except Exception as e:
            st.error(f"Error processing uploaded file: {e}")

    st.markdown("---")  # Divider

    # Upload section
    st.header("Upload Survey Questionnaires")

    uploaded_files = st.file_uploader(
        "Choose survey questionnaire files (TXT, JSON, CSV, DOCX, PDF)",
        type=['txt', 'json', 'csv', 'docx', 'pdf'],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        st.success(f"Uploaded {len(uploaded_files)} file(s)")

        # Display uploaded files
        for i, file in enumerate(st.session_state.uploaded_files):
            st.write(f"{i+1}. {file.name}")

    # Model selection
    st.header("Select AI Model for Analysis")

    # Create a list of model names for the dropdown
    model_names = [model['name'] for model in st.session_state.models]
    selected_model_name = st.selectbox("Choose an AI model for analysis", options=model_names, index=0)

    # Get the selected model object based on the name
    selected_model = next((model for model in st.session_state.models if model['name'] == selected_model_name), None)

    # Temperature control for the selected model
    if selected_model:
        st.subheader(f"Temperature for {selected_model['name']}")
        temperature = st.slider(
            f"Set temperature for {selected_model['name']}",
            min_value=0.0,
            max_value=1.0,
            value=selected_model['temperature'],
            step=0.1,
            key=f"temp_{selected_model['provider']}"
        )
        # Update the temperature in the session state
        selected_model['temperature'] = temperature
        st.caption("Temperature controls randomness. Lower values make responses more deterministic, higher values more creative.")

    # Analyze button
    if st.button("Analyze Survey Quality", type="primary"):
        if not st.session_state.uploaded_files:
            st.error("Please upload at least one survey questionnaire file")
        elif not selected_model:
            st.error("Please select an AI model")
        else:
            # Show loading status with detailed text
            # Show progress information
            progress_text = f"Starting analysis of {len(st.session_state.uploaded_files)} file(s) with {selected_model_name}..."
            st.info(progress_text)

            with st.spinner(f"Analyzing survey quality with {selected_model_name}..."):
                analyze_surveys([selected_model])

    # Results section
    st.header("Analysis Results")

    if st.session_state.analysis_results:
        st.success(f"Found {len(st.session_state.analysis_results)} analysis result(s)")

        for i, result in enumerate(st.session_state.analysis_results):
            with st.expander(f"Result {i+1}: {result['filename']}"):
                st.json(result['analysis'])

                # Download JSON button
                json_str = json.dumps(result['analysis'], indent=2)
                st.download_button(
                    label="Download JSON Result",
                    data=json_str,
                    file_name=f"analysis_result_{result['filename']}.json",
                    mime="application/json"
                )

                # Generate DOCX button
                if st.button(f"Generate DOCX for {result['filename']}", key=f"docx_{i}"):
                    docx_file = generate_docx(result['analysis'], result['filename'])
                    with open(docx_file, "rb") as f:
                        st.download_button(
                            label="Download DOCX Report",
                            data=f,
                            file_name=f"quality_report_{result['filename']}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
    else:
        st.info("No analysis results yet. Upload surveys and run analysis to see results here.")



def settings_section():
    st.header("Application Settings")

    st.subheader("Export Options")
    include_charts = st.checkbox("Include charts in DOCX export", value=True)
    detailed_analysis = st.checkbox("Include detailed analysis in export", value=True)

    st.subheader("AI Model Settings")
    # Allow setting default temperature for all models
    default_temperature = st.slider(
        "Default temperature for all AI models",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        key="default_temp_slider"
    )

    if st.button("Apply to all models"):
        for model in st.session_state.models:
            model['temperature'] = default_temperature
        st.success(f"Default temperature {default_temperature} applied to all models!")

    st.subheader("Quality Metrics")
    metrics = st.multiselect(
        "Select quality metrics to analyze:",
        ["Clarity", "Bias Detection", "Relevance", "Completeness", "Logical Flow", "Response Options", "Demographic Appropriateness"],
        default=["Clarity", "Bias Detection", "Relevance"]
    )

def analyze_surveys(selected_models):
    """Analyze uploaded surveys using selected AI models"""
    results = []

    # Show overall progress
    total_files = len(st.session_state.uploaded_files)
    for idx, uploaded_file in enumerate(st.session_state.uploaded_files):
        # Show progress for current file
        progress_text = f"Processing file {idx + 1} of {total_files}: {uploaded_file.name}..."
        st.info(progress_text)

        # Process different file types
        st.info(f"Extracting content from {uploaded_file.name}...")
        file_content = process_uploaded_file(uploaded_file)

        if not file_content:
            st.error(f"Could not process file: {uploaded_file.name}")
            continue

        st.success(f"Content extracted from {uploaded_file.name}, sending to AI model...")

        # Prepare analysis for each selected model
        file_analysis = {
            'filename': uploaded_file.name,
            'models_used': [],
            'individual_question_analysis': [],
            'recommendations': [],
            'overall_assessment': "",
            'timestamp': datetime.now().isoformat()
        }

        for model in selected_models:
            # Show progress for model analysis
            model_progress_text = f"Analyzing {uploaded_file.name} with {model['name']}..."
            st.info(model_progress_text)

            # Call AI model for analysis
            model_analysis = call_ai_model(file_content, model)
            file_analysis['models_used'].append({
                'model_name': model['name'],
                'analysis': model_analysis
            })

            # Process model analysis results
            if 'recommendations' in model_analysis:
                file_analysis['recommendations'].extend(model_analysis['recommendations'])

            # Include detailed analysis components if present
            if 'individual_question_analysis' in model_analysis:
                file_analysis['individual_question_analysis'].extend(model_analysis['individual_question_analysis'])

            if 'overall_assessment' in model_analysis:
                if file_analysis['overall_assessment']:
                    file_analysis['overall_assessment'] += f"\n\nAssessment by {model['name']}:\n{model_analysis['overall_assessment']}"
                else:
                    file_analysis['overall_assessment'] = f"Assessment by {model['name']}:\n{model_analysis['overall_assessment']}"

        results.append({
            'filename': uploaded_file.name,
            'analysis': file_analysis
        })

    st.session_state.analysis_results = results
    st.success(f"Analysis complete for {len(results)} file(s)!")

def process_uploaded_file(uploaded_file):
    """Process different file types and extract text content, including tables"""
    import fitz  # PyMuPDF for PDF processing
    import csv
    from io import StringIO, BytesIO

    file_extension = uploaded_file.name.split('.')[-1].lower()

    try:
        if file_extension == 'txt':
            return uploaded_file.getvalue().decode("utf-8")

        elif file_extension == 'json':
            content = uploaded_file.getvalue().decode("utf-8")
            json_data = json.loads(content)
            # Convert JSON to string for analysis
            return json.dumps(json_data, indent=2)

        elif file_extension == 'csv':
            string_data = StringIO(uploaded_file.getvalue().decode("utf-8"))
            csv_reader = csv.reader(string_data)
            content = '\n'.join([','.join(row) for row in csv_reader])
            return content

        elif file_extension == 'docx':
            from docx import Document
            doc = Document(BytesIO(uploaded_file.getvalue()))

            # Extract text content
            content = '\n'.join([paragraph.text for paragraph in doc.paragraphs])

            # Extract table content
            table_content = []
            for table in doc.tables:
                for row in table.rows:
                    row_data = [cell.text for cell in row.cells]
                    table_content.append('| ' + ' | '.join(row_data) + ' |')

            # Combine text and table content
            if table_content:
                content += "\n\nExtracted Tables:\n" + '\n'.join(table_content)

            return content

        elif file_extension == 'pdf':
            pdf_document = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
            content = ""

            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)

                # Extract regular text
                content += page.get_text() + "\n"

                # Extract tables using PyMuPDF's table functionality
                try:
                    tables = page.find_tables()
                    for i, table in enumerate(tables):
                        content += f"\nTable {i+1}:\n"
                        for row in table.rows:
                            row_text = " | ".join([cell.text.strip() for cell in row.cells])
                            content += f"{row_text}\n"
                        content += "\n"
                except:
                    # If table extraction fails, continue with just text
                    pass

            pdf_document.close()
            return content

        else:
            st.error(f"Unsupported file type: {file_extension}")
            return None

    except Exception as e:
        st.error(f"Error processing file {uploaded_file.name}: {str(e)}")
        return None

def call_ai_model(file_content, model):
    """Call the specified AI model for analysis"""
    headers = {}
    payload = {}

    if model['provider'] == 'deepseek':
        # DeepSeek Reasoner API call
        headers = {
            'Authorization': f"Bearer {model['api_key']}",
            'Content-Type': 'application/json'
        }
        prompt = get_deepseek_prompt(file_content)
        payload = {
            "model": "deepseek-reasoner",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "response_format": {"type": "json_object"},
            "temperature": model.get('temperature', 0.3)
        }
        url = model.get('endpoint') or 'https://api.deepseek.com/chat/completions'

    elif model['provider'] in ['gemini3', 'gemini25']:
        # For Gemini models, we use the Google Generative AI library
        import google.generativeai as genai
        genai.configure(api_key=model['api_key'])

        # Select appropriate model
        if model['provider'] == 'gemini3':
            model_name = "gemini-3.0-flash"
        else:
            model_name = "gemini-2.5-flash"

        gemini_model = genai.GenerativeModel(
            model_name,
            generation_config={
                "temperature": model.get('temperature', 0.3),
                "response_mime_type": "application/json"
            }
        )

        prompt = get_gemini_prompt(file_content)

        try:
            # Show status that document has been sent to Gemini
            st.info(f"Document sent to {model['name']}, waiting for response...")
            response = gemini_model.generate_content(
                [prompt]  # Pass as a list
            )
            # Show status that response has been received
            st.success(f"Response received from {model['name']}")

            # Parse the JSON response from Gemini
            try:
                analysis = json.loads(response.text if hasattr(response, 'text') else str(response))
            except json.JSONDecodeError:
                # If content is not valid JSON, wrap it in our expected format
                analysis = {
                    "individual_question_analysis": [],
                    "overall_assessment": response.text if hasattr(response, 'text') else str(response),
                    "recommendations": ["This model did not return structured JSON. Raw analysis: " + (response.text if hasattr(response, 'text') else str(response))]
                }
            return analysis
        except Exception as e:
            st.error(f"Error calling {model['name']}: {str(e)}")
            return {
                "individual_question_analysis": [],
                "overall_assessment": "",
                "recommendations": [f"Error analyzing with {model['name']}: {str(e)}"]
            }

    elif model['provider'] == 'openrouter':
        # OpenRouter API call for Xiaomi/MIMO model
        headers = {
            'Authorization': f"Bearer {model['api_key']}",
            'Content-Type': 'application/json'
        }
        prompt = get_openrouter_prompt(file_content)
        payload = {
            "model": "xiaomi/mimo-v2-flash:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": model.get('temperature', 0.3)
        }
        url = model.get('endpoint') or 'https://openrouter.ai/api/v1/chat/completions'

        try:
            # Show status that document has been sent to the model
            st.info(f"Document sent to {model['name']}, waiting for response...")
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            # Show status that response has been received
            st.success(f"Response received from {model['name']}")

            # Extract the content from the response
            content = result['choices'][0]['message']['content']

            # Try to parse as JSON, but handle if it's not valid JSON
            try:
                analysis = json.loads(content)
            except json.JSONDecodeError:
                # If content is not valid JSON, wrap it in our expected format
                analysis = {
                    "individual_question_analysis": [],
                    "overall_assessment": content,
                    "recommendations": ["This model did not return structured JSON. Raw analysis: " + content]
                }

            return analysis
        except Exception as e:
            st.error(f"Error calling {model['name']}: {str(e)}")
            return {
                "quality_metrics": {},
                "recommendations": [f"Error analyzing with {model['name']}: {str(e)}"],
                "detailed_analysis": f"Error occurred: {str(e)}"
            }

    # DeepSeek and Generic API calls (both expect JSON responses)
    headers = {
        'Authorization': f"Bearer {model['api_key']}",
        'Content-Type': 'application/json'
    }

    if model['provider'] == 'deepseek':
        prompt = get_deepseek_prompt(file_content)
        payload = {
            "model": "deepseek-reasoner",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "response_format": {"type": "json_object"},
            "temperature": model.get('temperature', 0.3)
        }
        url = model.get('endpoint') or 'https://api.deepseek.com/chat/completions'
    else:  # Generic model
        prompt = get_generic_prompt(file_content)
        payload = {
            "model": model.get('model_name', 'custom-model'),
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "response_format": {"type": "json_object"},
            "temperature": model.get('temperature', 0.3)
        }
        url = model.get('endpoint') or 'https://api.openai.com/v1/chat/completions'

    try:
        # Show status that document has been sent to the model
        st.info(f"Document sent to {model['name']}, waiting for response...")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        # Show status that response has been received
        st.success(f"Response received from {model['name']}")

        # Extract the content from the response
        content = result['choices'][0]['message']['content']

        # Parse the JSON response
        try:
            analysis = json.loads(content)
        except json.JSONDecodeError:
            # If content is not valid JSON, wrap it in our expected format
            analysis = {
                "individual_question_analysis": [],
                "overall_assessment": content,
                "recommendations": ["This model did not return structured JSON. Raw analysis: " + content]
            }

        return analysis
    except Exception as e:
        st.error(f"Error calling {model['name']}: {str(e)}")
        return {
            "individual_question_analysis": [],
            "overall_assessment": "",
            "recommendations": [f"Error analyzing with {model['name']}: {str(e)}"]
        }

def generate_docx(analysis_data, filename):
    """Generate a DOCX report from analysis data"""
    doc = Document()

    # Title
    doc.add_heading('Survey Questionnaire Quality Report', 0)
    doc.add_paragraph(f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    doc.add_paragraph(f'Analyzed File: {filename}')

    # Add individual question analysis if present
    if 'individual_question_analysis' in analysis_data and analysis_data['individual_question_analysis']:
        doc.add_heading('Individual Question Analysis', level=1)
        for question in analysis_data['individual_question_analysis']:
            question_text = question.get('question_text', 'N/A')
            validity = question.get('validity', 'N/A')
            reason = question.get('reason', 'N/A')
            table_number = question.get('table_number', 'N/A')
            item_number = question.get('item_number', 'N/A')
            variable_name = question.get('variable_name', 'N/A')

            doc.add_paragraph(f"Table {table_number}, Item {item_number} (Variable: {variable_name}): {question_text}", style='List Bullet')
            doc.add_paragraph(f"  Validity: {validity}", style='List Bullet')
            doc.add_paragraph(f"  Reason: {reason}", style='List Bullet')

            # Add alternative question if present and the question is not valid
            alternative_question = question.get('alternative_question', '')
            if alternative_question and validity.lower() == 'not valid':
                doc.add_paragraph(f"  Suggested Alternative: {alternative_question}", style='List Bullet')

            # Add duplicate information if present
            duplicates_with = question.get('duplicates_with', [])
            if duplicates_with:
                doc.add_paragraph(f"  Duplicates with:", style='List Bullet')
                for dup in duplicates_with:
                    dup_table = dup.get('table_number', 'N/A')
                    dup_item = dup.get('item_number', 'N/A')
                    dup_text = dup.get('question_text', 'N/A')
                    doc.add_paragraph(f"    Table {dup_table}, Item {dup_item}: {dup_text}", style='List Bullet')

            doc.add_paragraph("")  # Empty line for spacing

    doc.add_heading('Overall Assessment', level=1)

    # Add overall assessment
    if 'overall_assessment' in analysis_data:
        doc.add_paragraph(analysis_data['overall_assessment'])

    doc.add_heading('General Recommendations', level=1)

    # Add general recommendations
    if 'recommendations' in analysis_data and analysis_data['recommendations']:
        for rec in analysis_data['recommendations']:
            doc.add_paragraph(rec, style='List Bullet')

    # Save to temporary file
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, f"quality_report_{filename.replace('.txt', '').replace('.json', '')}.docx")
    doc.save(temp_path)

    return temp_path

if __name__ == "__main__":
    main()