#!/usr/bin/env python
"""
Test script to verify that the JSON extraction works with the new structure
"""

import json
from app import extract_valid_json

def test_json_extraction():
    """Test JSON extraction with the new structure"""
    
    # Test with a sample JSON that includes the new survey_general_instructions_analysis
    sample_json = '''
    {
        "survey_general_instructions_analysis": {
            "instructions_present": true,
            "scale_correctly_defined": true,
            "scale_definition_text": "4 - Strongly Agree, 3 - Agree, 2 - Disagree, 1 - Strongly Disagree",
            "general_instructions_text": "Please rate each statement using the following scale:",
            "issues_found": [],
            "recommendations": []
        },
        "individual_question_analysis": [
            {
                "question_id": "Q1",
                "table_number": "1",
                "item_number": "1",
                "variable_name": "Service Quality",
                "question_text": "The service was excellent.",
                "validity": "Valid",
                "reason": "Clear and appropriate question",
                "alternative_question": "",
                "duplicates_with": []
            }
        ],
        "overall_assessment": "The survey is well-structured with appropriate questions.",
        "recommendations": ["Consider adding more questions for better coverage."]
    }
    '''
    
    result = extract_valid_json(sample_json)
    
    assert result is not None, "Should extract valid JSON"
    assert "survey_general_instructions_analysis" in result, "Should contain general instructions analysis"
    assert "individual_question_analysis" in result, "Should contain individual question analysis"
    assert result["survey_general_instructions_analysis"]["instructions_present"] == True, "Instructions should be present"
    assert len(result["individual_question_analysis"]) == 1, "Should have one question analysis"
    
    print("[PASS] JSON extraction with new structure works correctly")

def test_json_extraction_with_markdown():
    """Test JSON extraction when wrapped in markdown"""
    
    sample_with_markdown = '''
    Here is the analysis:
    ```json
    {
        "survey_general_instructions_analysis": {
            "instructions_present": false,
            "scale_correctly_defined": false,
            "scale_definition_text": "",
            "general_instructions_text": "",
            "issues_found": ["Scale not properly defined"],
            "recommendations": ["Define the scale clearly"]
        },
        "individual_question_analysis": [],
        "overall_assessment": "Needs improvement",
        "recommendations": ["Fix the scale definition"]
    }
    ```
    '''
    
    result = extract_valid_json(sample_with_markdown)
    
    assert result is not None, "Should extract JSON from markdown"
    assert "survey_general_instructions_analysis" in result, "Should contain general instructions analysis"
    assert result["survey_general_instructions_analysis"]["scale_correctly_defined"] == False, "Scale should not be correctly defined"
    
    print("[PASS] JSON extraction with markdown works correctly")

def test_partial_json_extraction():
    """Test extraction when there's extra text around the JSON"""
    
    sample_partial = '''
    Some introductory text here...
    {
        "survey_general_instructions_analysis": {
            "instructions_present": true,
            "scale_correctly_defined": true,
            "scale_definition_text": "4 - Strongly Agree, 3 - Agree, 2 - Disagree, 1 - Strongly Disagree",
            "general_instructions_text": "Please rate each statement using the following scale:",
            "issues_found": [],
            "recommendations": []
        },
        "individual_question_analysis": [],
        "overall_assessment": "Good survey",
        "recommendations": []
    }
    Some concluding text here...
    '''
    
    result = extract_valid_json(sample_partial)
    
    assert result is not None, "Should extract JSON from text with surrounding content"
    assert "survey_general_instructions_analysis" in result, "Should contain general instructions analysis"
    assert result["survey_general_instructions_analysis"]["instructions_present"] == True, "Instructions should be present"
    
    print("[PASS] Partial JSON extraction works correctly")

def run_tests():
    """Run all JSON extraction tests"""
    print("Testing JSON extraction functionality...")
    
    test_json_extraction()
    test_json_extraction_with_markdown()
    test_partial_json_extraction()
    
    print("\n[SUCCESS] All JSON extraction tests passed!")

if __name__ == "__main__":
    run_tests()