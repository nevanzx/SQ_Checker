#!/usr/bin/env python
"""
Final integration test to verify the complete workflow works with the new general instructions checking
"""

import json
from prompts import get_survey_system_prompt, get_survey_user_prompt, get_deepseek_prompt
from app import extract_valid_json

def test_complete_workflow():
    """Test the complete workflow from prompt creation to JSON extraction"""
    
    # Create a sample survey with general instructions
    sample_survey_with_instructions = """
    Survey: Customer Experience
    
    General Instructions:
    Please read each statement carefully and indicate your level of agreement using the following scale:
    4 - Strongly Agree
    3 - Agree
    2 - Disagree
    1 - Strongly Disagree
    
    Variables:
    Service Quality: Measures customer perception of service excellence
    
    Table 1: Service Quality
    1. The staff were courteous and helpful.
    2. The service was timely and efficient.
    3. The staff lacked basic courtesy.
    """
    
    # Get the complete prompt structure
    messages = get_deepseek_prompt(sample_survey_with_instructions)
    
    # Verify the system message contains the new instructions
    system_content = messages[0]['content']
    assert 'GENERAL INSTRUCTIONS SECTION' in system_content
    assert 'survey_general_instructions_analysis' in system_content
    assert 'instructions_present' in system_content
    
    # Verify the user message contains the survey content
    user_content = messages[1]['content']
    assert 'Customer Experience' in user_content
    assert 'Strongly Agree' in user_content
    
    print("[PASS] Complete workflow - Prompt generation works correctly")
    
    # Test with a sample JSON response that would come from the AI
    ai_response_simulation = '''
    {
        "survey_general_instructions_analysis": {
            "instructions_present": true,
            "scale_correctly_defined": true,
            "scale_definition_text": "4 - Strongly Agree\\n3 - Agree\\n2 - Disagree\\n1 - Strongly Disagree",
            "general_instructions_text": "Please read each statement carefully and indicate your level of agreement using the following scale:\\n4 - Strongly Agree\\n3 - Agree\\n2 - Disagree\\n1 - Strongly Disagree",
            "issues_found": [],
            "recommendations": []
        },
        "individual_question_analysis": [
            {
                "question_id": "SQ_01",
                "table_number": "1",
                "item_number": "1",
                "variable_name": "Service Quality",
                "question_text": "The staff were courteous and helpful.",
                "validity": "Valid",
                "reason": "Clear, positive statement appropriate for the variable",
                "alternative_question": "",
                "duplicates_with": []
            },
            {
                "question_id": "SQ_02", 
                "table_number": "1",
                "item_number": "2",
                "variable_name": "Service Quality",
                "question_text": "The service was timely and efficient.",
                "validity": "Valid",
                "reason": "Clear, positive statement appropriate for the variable",
                "alternative_question": "",
                "duplicates_with": []
            },
            {
                "question_id": "SQ_03",
                "table_number": "1", 
                "item_number": "3",
                "variable_name": "Service Quality",
                "question_text": "The staff lacked basic courtesy.",
                "validity": "Not Valid",
                "reason": "Negatively phrased question that conflicts with positive framing of variable",
                "alternative_question": "The staff demonstrated basic courtesy.",
                "duplicates_with": []
            }
        ],
        "overall_assessment": "The survey has good questions overall, but one negatively phrased question should be revised.",
        "recommendations": ["Rephrase negatively worded questions to maintain positive framing"]
    }
    '''
    
    # Extract the JSON
    extracted = extract_valid_json(ai_response_simulation)
    
    # Verify the extraction worked
    assert extracted is not None
    assert 'survey_general_instructions_analysis' in extracted
    assert 'individual_question_analysis' in extracted
    assert extracted['survey_general_instructions_analysis']['instructions_present'] == True
    assert extracted['survey_general_instructions_analysis']['scale_correctly_defined'] == True
    assert len(extracted['individual_question_analysis']) == 3
    
    print("[PASS] Complete workflow - JSON extraction works correctly")
    
    # Verify the general instructions analysis has the expected structure
    gen_analysis = extracted['survey_general_instructions_analysis']
    expected_fields = ['instructions_present', 'scale_correctly_defined', 'scale_definition_text', 
                      'general_instructions_text', 'issues_found', 'recommendations']
    
    for field in expected_fields:
        assert field in gen_analysis, f"Field {field} should be in general instructions analysis"
    
    print("[PASS] Complete workflow - General instructions analysis structure is correct")
    
    print("\n[SUCCESS] Complete workflow test passed!")

def test_edge_cases():
    """Test edge cases for the new functionality"""
    
    # Test with missing scale definition
    ai_response_missing_scale = '''
    {
        "survey_general_instructions_analysis": {
            "instructions_present": true,
            "scale_correctly_defined": false,
            "scale_definition_text": "",
            "general_instructions_text": "Please answer all questions.",
            "issues_found": ["Scale not properly defined"],
            "recommendations": ["Define the scale clearly as 4-Strongly Agree, 3-Agree, 2-Disagree, 1-Strongly Disagree"]
        },
        "individual_question_analysis": [],
        "overall_assessment": "Survey needs proper scale definition.",
        "recommendations": ["Add proper scale definition"]
    }
    '''
    
    extracted = extract_valid_json(ai_response_missing_scale)
    assert extracted is not None
    assert extracted['survey_general_instructions_analysis']['scale_correctly_defined'] == False
    assert len(extracted['survey_general_instructions_analysis']['issues_found']) > 0
    
    print("[PASS] Edge case - Missing scale definition handled correctly")
    
    # Test with malformed JSON that should still be extracted
    malformed_but_extractable = '''
    Some text before
    {
        "survey_general_instructions_analysis": {
            "instructions_present": false,
            "scale_correctly_defined": false,
            "scale_definition_text": "",
            "general_instructions_text": "",
            "issues_found": ["No general instructions found in survey"],
            "recommendations": ["Add general instructions with proper scale definition"]
        },
        "individual_question_analysis": [{"question_id": "Q1", "validity": "Valid", "reason": "Test"}],
        "overall_assessment": "Basic survey",
        "recommendations": ["Improve instructions"]
    }
    Some text after
    '''
    
    extracted = extract_valid_json(malformed_but_extractable)
    assert extracted is not None
    assert 'survey_general_instructions_analysis' in extracted
    
    print("[PASS] Edge case - Malformed JSON with surrounding text handled correctly")
    
    print("\n[SUCCESS] Edge cases test passed!")

def run_integration_tests():
    """Run all integration tests"""
    print("Running integration tests for the general instructions enhancement...\n")
    
    test_complete_workflow()
    print()
    test_edge_cases()
    
    print("\n[OVERALL SUCCESS] All integration tests passed! The general instructions checking enhancement is working correctly.")

if __name__ == "__main__":
    run_integration_tests()