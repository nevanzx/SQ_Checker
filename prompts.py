"""
AI Evaluation Prompts for Survey Quality Checker
This file contains all the prompts used for AI evaluation of survey questionnaires
"""

def get_survey_analysis_prompt(file_content):
    """
    General prompt for survey analysis
    """
    return f"""
    Analyze this survey questionnaire focusing on the validity of each question. For each question, determine if it is "Valid" or "Not Valid" with specific reasons.

    CRITICAL: Pay special attention to tables in the survey. For each table:
    - Check the top of the table for contextual statements like "As a young adult I..." or similar
    - Identify the variable name from the contextual statement that applies to all questions in that table
    - Analyze each question in the table considering the variable context provided by the header statement
    - Determine if each question is appropriate given the variable context provided by the header statement
    - Examine the relationship between the contextual statement and individual questions in the table
    - EACH table MUST be a 4pts likert scale questions
    - The Questions INCLUDING THE SUGGESTED ALTERNATIVE QUESTION must be POSITIVELY FRAMED IN THE CONTEXT OF THE VARIABLE DEFINITION.
    - ALTERNATIVE QUESTION SHOULD NOT BE THE SAME AS OTHER QUESTIONS.

    For each individual question, provide a "Valid" or "Not Valid" assessment with reasons including:
    - Whether the question has duplicate meaning with other questions (with reference to table number and question item number of the duplicate)
    - Whether the question is negatively phrased inappropriately relative to the variable
    - Any other validity concerns

    If a question is "Not Valid", suggest an alternative question based on the definition of each variable and the contextual statement that applies to the table. The alternative question should address the same concept but in a valid way.

    You MUST respond in valid JSON format with this exact structure:
    {{
        "individual_question_analysis": [
            {{
                "question_id": "unique_identifier_for_question",
                "table_number": "table_number_containing_question",
                "item_number": "item_number_within_table",
                "variable_name": "name_of_the_variable_from_contextual_statement",
                "question_text": "exact_question_text",
                "validity": "Valid or Not Valid",
                "reason": "specific_reason_for_validity_assessment",
                "alternative_question": "suggested_alternative_question_if_invalid_or_empty_string_if_valid",
                "duplicates_with": [
                    {{
                        "table_number": "table_number_of_duplicate",
                        "item_number": "item_number_of_duplicate",
                        "question_text": "text_of_duplicate_question"
                    }}
                ]
            }}
        ],
        "overall_assessment": "comprehensive_overall_assessment",
        "recommendations": [
            "specific_recommendation_1",
            "specific_recommendation_2"
        ]
    }}

    Survey content: {file_content}
    """


def get_deepseek_prompt(file_content):
    """
    Unified prompt for DeepSeek Reasoner (same as general prompt)
    """
    return get_survey_analysis_prompt(file_content)


def get_gemini_prompt(file_content):
    """
    Prompt specifically tailored for Google Gemini models
    """
    return f"""
    Analyze this survey questionnaire focusing on the validity of each question. For each question, determine if it is "Valid" or "Not Valid" with specific reasons.

    CRITICAL: Pay special attention to tables in the survey. For each table:
    - Check the top of the table for contextual statements like "As a young adult I..." or similar
    - Identify the variable name from the contextual statement that applies to all questions in that table
    - Analyze each question in the table considering the variable context provided by the header statement
    - Determine if each question is appropriate given the variable context provided by the header statement
    - Examine the relationship between the contextual statement and individual questions in the table
    - EACH table MUST be a 4pts likert scale questions
    - The Questions INCLUDING THE SUGGESTED ALTERNATIVE QUESTION must be POSITIVELY FRAMED IN THE CONTEXT OF THE VARIABLE DEFINITION.
    - ALTERNATIVE QUESTION SHOULD NOT BE THE SAME AS OTHER QUESTIONS.

    For each individual question, provide a "Valid" or "Not Valid" assessment with reasons including:
    - Whether the question has duplicate meaning with other questions (with reference to table number and question item number of the duplicate)
    - Whether the question is negatively phrased inappropriately relative to the variable
    - Any other validity concerns

    If a question is "Not Valid", suggest an alternative question based on the definition of each variable and the contextual statement that applies to the table. The alternative question should address the same concept but in a valid way.

    You MUST respond in valid JSON format with this exact structure:
    {{
        "individual_question_analysis": [
            {{
                "question_id": "unique_identifier_for_question",
                "table_number": "table_number_containing_question",
                "item_number": "item_number_within_table",
                "variable_name": "name_of_the_variable_from_contextual_statement",
                "question_text": "exact_question_text",
                "validity": "Valid or Not Valid",
                "reason": "specific_reason_for_validity_assessment",
                "alternative_question": "suggested_alternative_question_if_invalid_or_empty_string_if_valid",
                "duplicates_with": [
                    {{
                        "table_number": "table_number_of_duplicate",
                        "item_number": "item_number_of_duplicate",
                        "question_text": "text_of_duplicate_question"
                    }}
                ]
            }}
        ],
        "overall_assessment": "comprehensive_overall_assessment",
        "recommendations": [
            "specific_recommendation_1",
            "specific_recommendation_2"
        ]
    }}

    Survey content: {file_content}
    """


def get_openrouter_prompt(file_content):
    """
    Unified prompt for OpenRouter models (same as general prompt)
    """
    return get_survey_analysis_prompt(file_content)


def get_generic_prompt(file_content):
    """
    Unified prompt for other AI models (same as general prompt)
    """
    return get_survey_analysis_prompt(file_content)