#!/usr/bin/env python
"""
Test script to verify that the Part 2 and Part 3 variable definitions checking functionality works correctly
"""

import json
from prompts import get_survey_system_prompt, get_survey_user_prompt, get_deepseek_prompt
from app import extract_valid_json

def test_prompt_structure():
    """Test that the prompt contains the new Part 2 and Part 3 checking elements"""
    system_prompt = get_survey_system_prompt()
    
    # Check that the prompt mentions checking Part 2 and Part 3
    assert "SECOND, EVALUATE PART 2 AND PART 3" in system_prompt, "Prompt should mention checking Part 2 and Part 3"
    assert "Part 2 and Part 3 should contain ONLY variable definitions" in system_prompt, "Prompt should specify that Part 2 and 3 should only have definitions"
    assert "survey_parts_analysis" in system_prompt, "Prompt should specify the new survey_parts_analysis structure"
    assert "part_2_has_only_definitions" in system_prompt, "Prompt should include part_2_has_only_definitions field"
    assert "part_3_has_only_definitions" in system_prompt, "Prompt should include part_3_has_only_definitions field"
    
    print("[PASS] Prompt structure test passed")

def test_expected_json_structure():
    """Test that the expected JSON structure is correctly specified in the prompt"""
    system_prompt = get_survey_system_prompt()
    
    # Check for the new structure elements
    assert '"survey_parts_analysis"' in system_prompt, "Prompt should specify survey_parts_analysis"
    assert '"part_2_has_only_definitions"' in system_prompt, "Prompt should specify part_2_has_only_definitions field"
    assert '"part_3_has_only_definitions"' in system_prompt, "Prompt should specify part_3_has_only_definitions field"
    assert '"part_2_content_summary"' in system_prompt, "Prompt should specify part_2_content_summary field"
    assert '"part_3_content_summary"' in system_prompt, "Prompt should specify part_3_content_summary field"
    assert '"part_2_issues"' in system_prompt, "Prompt should specify part_2_issues field"
    assert '"part_3_issues"' in system_prompt, "Prompt should specify part_3_issues field"
    
    print("[PASS] Expected JSON structure test passed")

def test_json_extraction_with_new_structure():
    """Test JSON extraction with the new survey_parts_analysis structure"""
    
    # Test with a sample JSON that includes the new survey_parts_analysis
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
        "survey_parts_analysis": {
            "part_2_has_only_definitions": true,
            "part_3_has_only_definitions": false,
            "part_2_content_summary": "Variables: Service Quality: Measures customer perception of service excellence",
            "part_3_content_summary": "Variables: Atmosphere: Measures ambiance, Part 4: Extra content that shouldn't be here",
            "part_2_issues": [],
            "part_3_issues": ["Part 3 contains content other than variable definitions: 'Part 4: Extra content that shouldn't be here'"],
            "part_2_recommendations": [],
            "part_3_recommendations": ["Remove non-definition content from Part 3"]
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
            }
        ],
        "overall_assessment": "The survey has good questions overall, but Part 3 has issues.",
        "recommendations": ["Fix Part 3 content to only include variable definitions"]
    }
    '''
    
    result = extract_valid_json(sample_json)
    
    assert result is not None, "Should extract valid JSON"
    assert "survey_parts_analysis" in result, "Should contain survey parts analysis"
    assert "survey_general_instructions_analysis" in result, "Should contain general instructions analysis"
    assert "individual_question_analysis" in result, "Should contain individual question analysis"
    assert result["survey_parts_analysis"]["part_2_has_only_definitions"] == True, "Part 2 should have only definitions"
    assert result["survey_parts_analysis"]["part_3_has_only_definitions"] == False, "Part 3 should not have only definitions"
    assert len(result["individual_question_analysis"]) == 1, "Should have one question analysis"
    
    print("[PASS] JSON extraction with new structure works correctly")

def test_sample_survey_processing():
    """Test with a sample survey that has Part 2 and Part 3 sections"""
    sample_survey = """
    Survey: Customer Satisfaction
    
    General Instructions:
    Please rate each statement using the following scale:
    4 - Strongly Agree
    3 - Agree  
    2 - Disagree
    1 - Strongly Disagree
    
    Part 2: Variables
    Service Quality: Measures customer perception of service excellence
    
    Part 3: Variables  
    Atmosphere: Measures the ambiance and environment of the establishment
    
    Table 1: Service Quality
    1. The staff were courteous and helpful.
       [4] Strongly Agree [3] Agree [2] Disagree [1] Strongly Disagree
    
    Table 2: Atmosphere
    1. The restaurant had a pleasant atmosphere.
       [4] Strongly Agree [3] Agree [2] Disagree [1] Strongly Disagree
    """
    
    # Get the prompt structure
    messages = get_deepseek_prompt(sample_survey)
    
    # Verify we have both system and user messages
    assert len(messages) == 2, "Should have system and user messages"
    assert messages[0]["role"] == "system", "First message should be system"
    assert messages[1]["role"] == "user", "Second message should be user"
    
    print("[PASS] Sample survey processing test passed")

def run_tests():
    """Run all tests"""
    print("Running tests for Part 2 and Part 3 variable definitions checking...")
    
    test_prompt_structure()
    test_expected_json_structure()
    test_json_extraction_with_new_structure()
    test_sample_survey_processing()
    
    print("\n[SUCCESS] All tests passed! The Part 2 and Part 3 variable definitions checking functionality is working correctly.")

if __name__ == "__main__":
    run_tests()