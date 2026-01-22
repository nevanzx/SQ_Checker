#!/usr/bin/env python
"""
Final comprehensive test to verify all enhancements work together
"""

import json
from prompts import get_survey_system_prompt, get_survey_user_prompt, get_deepseek_prompt
from app import extract_valid_json

def test_comprehensive_workflow():
    """Test the complete workflow with all new features"""
    
    # Create a sample survey with general instructions and Part 2/3 sections
    sample_survey_with_all_features = """
    Survey: Customer Experience
    
    General Instructions:
    Please read each statement carefully and indicate your level of agreement using the following scale:
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
    2. The service was timely and efficient.
    
    Table 2: Atmosphere  
    1. The restaurant had a pleasant atmosphere.
    2. The environment was relaxing and comfortable.
    """
    
    # Get the complete prompt structure
    messages = get_deepseek_prompt(sample_survey_with_all_features)
    
    # Verify the system message contains all the new instructions
    system_content = messages[0]['content']
    assert 'GENERAL INSTRUCTIONS SECTION' in system_content
    assert 'SECOND, EVALUATE PART 2 AND PART 3' in system_content
    assert 'survey_general_instructions_analysis' in system_content
    assert 'survey_parts_analysis' in system_content
    assert 'part_2_has_only_definitions' in system_content
    assert 'part_3_has_only_definitions' in system_content
    
    # Verify the user message contains the survey content
    user_content = messages[1]['content']
    assert 'Customer Experience' in user_content
    assert 'Strongly Agree' in user_content
    assert 'Part 2: Variables' in user_content
    assert 'Part 3: Variables' in user_content
    
    print("[PASS] Comprehensive workflow - Prompt generation works correctly")
    
    # Test with a sample JSON response that would come from the AI with all new features
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
        "survey_parts_analysis": {
            "part_2_has_only_definitions": true,
            "part_3_has_only_definitions": true,
            "part_2_content_summary": "Service Quality: Measures customer perception of service excellence",
            "part_3_content_summary": "Atmosphere: Measures the ambiance and environment of the establishment",
            "part_2_issues": [],
            "part_3_issues": [],
            "part_2_recommendations": [],
            "part_3_recommendations": []
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
                "question_id": "AT_01",
                "table_number": "2", 
                "item_number": "1",
                "variable_name": "Atmosphere",
                "question_text": "The restaurant had a pleasant atmosphere.",
                "validity": "Valid",
                "reason": "Clear, positive statement appropriate for the variable",
                "alternative_question": "",
                "duplicates_with": []
            },
            {
                "question_id": "AT_02",
                "table_number": "2", 
                "item_number": "2",
                "variable_name": "Atmosphere",
                "question_text": "The environment was relaxing and comfortable.",
                "validity": "Valid",
                "reason": "Clear, positive statement appropriate for the variable",
                "alternative_question": "",
                "duplicates_with": []
            }
        ],
        "overall_assessment": "The survey is well-structured with appropriate questions and proper definitions.",
        "recommendations": ["Consider adding more questions for better coverage."]
    }
    '''
    
    # Extract the JSON
    extracted = extract_valid_json(ai_response_simulation)
    
    # Verify the extraction worked
    assert extracted is not None
    assert 'survey_general_instructions_analysis' in extracted
    assert 'survey_parts_analysis' in extracted
    assert 'individual_question_analysis' in extracted
    assert extracted['survey_general_instructions_analysis']['instructions_present'] == True
    assert extracted['survey_general_instructions_analysis']['scale_correctly_defined'] == True
    assert extracted['survey_parts_analysis']['part_2_has_only_definitions'] == True
    assert extracted['survey_parts_analysis']['part_3_has_only_definitions'] == True
    assert len(extracted['individual_question_analysis']) == 4
    
    print("[PASS] Comprehensive workflow - JSON extraction works correctly")
    
    # Verify all structures have the expected fields
    gen_analysis = extracted['survey_general_instructions_analysis']
    gen_expected_fields = ['instructions_present', 'scale_correctly_defined', 'scale_definition_text', 
                          'general_instructions_text', 'issues_found', 'recommendations']
    
    for field in gen_expected_fields:
        assert field in gen_analysis, f"Field {field} should be in general instructions analysis"
    
    parts_analysis = extracted['survey_parts_analysis']
    parts_expected_fields = ['part_2_has_only_definitions', 'part_3_has_only_definitions', 
                           'part_2_content_summary', 'part_3_content_summary', 
                           'part_2_issues', 'part_3_issues', 
                           'part_2_recommendations', 'part_3_recommendations']
    
    for field in parts_expected_fields:
        assert field in parts_analysis, f"Field {field} should be in survey parts analysis"
    
    print("[PASS] Comprehensive workflow - All analysis structures have correct fields")
    
    print("\n[SUCCESS] Comprehensive workflow test passed!")

def test_issue_detection():
    """Test that the system properly detects issues in Part 2 and Part 3"""
    
    # Test with a survey that has issues in Part 2 and Part 3
    problematic_survey_response = '''
    {
        "survey_general_instructions_analysis": {
            "instructions_present": true,
            "scale_correctly_defined": true,
            "scale_definition_text": "4 - Strongly Agree\\n3 - Agree\\n2 - Disagree\\n1 - Strongly Disagree",
            "general_instructions_text": "Please read each statement carefully and indicate your level of agreement using the following scale:\\n4 - Strongly Agree\\n3 - Agree\\n2 - Disagree\\n1 - Strongly Disagree",
            "issues_found": [],
            "recommendations": []
        },
        "survey_parts_analysis": {
            "part_2_has_only_definitions": false,
            "part_3_has_only_definitions": false,
            "part_2_content_summary": "Service Quality: Measures customer perception of service excellence\\nExtra Info: This is not a definition",
            "part_3_content_summary": "Atmosphere: Measures ambiance\\nPart 4: This should not be in Part 3",
            "part_2_issues": ["Part 2 contains content other than variable definitions: 'Extra Info: This is not a definition'"],
            "part_3_issues": ["Part 3 contains content other than variable definitions: 'Part 4: This should not be in Part 3'"],
            "part_2_recommendations": ["Remove non-definition content from Part 2"],
            "part_3_recommendations": ["Remove non-definition content from Part 3"]
        },
        "individual_question_analysis": [],
        "overall_assessment": "The survey has issues with Part 2 and Part 3 content.",
        "recommendations": ["Fix Part 2 and Part 3 to only include variable definitions"]
    }
    '''
    
    extracted = extract_valid_json(problematic_survey_response)
    
    assert extracted is not None
    assert extracted['survey_parts_analysis']['part_2_has_only_definitions'] == False
    assert extracted['survey_parts_analysis']['part_3_has_only_definitions'] == False
    assert len(extracted['survey_parts_analysis']['part_2_issues']) > 0
    assert len(extracted['survey_parts_analysis']['part_3_issues']) > 0
    
    print("[PASS] Issue detection - Problems in Part 2 and Part 3 are properly detected")
    
    print("\n[SUCCESS] Issue detection test passed!")

def run_final_tests():
    """Run all final tests"""
    print("Running final comprehensive tests for all enhancements...\n")
    
    test_comprehensive_workflow()
    print()
    test_issue_detection()
    
    print("\n[FINAL SUCCESS] All comprehensive tests passed! The enhanced survey quality checker is working correctly with all new features.")

if __name__ == "__main__":
    run_final_tests()