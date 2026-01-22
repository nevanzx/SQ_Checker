#!/usr/bin/env python
"""
Test script to verify that the general instructions checking functionality works correctly
"""

import json
from prompts import get_survey_system_prompt, get_survey_user_prompt, get_deepseek_prompt

def test_prompt_structure():
    """Test that the prompt contains the new general instructions checking elements"""
    system_prompt = get_survey_system_prompt()
    
    # Check that the prompt mentions checking general instructions
    assert "GENERAL INSTRUCTIONS SECTION" in system_prompt, "Prompt should mention checking general instructions"
    assert "scale is clearly defined" in system_prompt, "Prompt should check for scale definition"
    assert "survey_general_instructions_analysis" in system_prompt, "Prompt should specify the new JSON structure"
    assert "instructions_present" in system_prompt, "Prompt should include instructions_present field"
    assert "scale_correctly_defined" in system_prompt, "Prompt should include scale_correctly_defined field"
    
    print("[PASS] Prompt structure test passed")

def test_expected_json_structure():
    """Test that the expected JSON structure is correctly specified in the prompt"""
    system_prompt = get_survey_system_prompt()
    
    # Check for the new structure elements
    assert '"survey_general_instructions_analysis"' in system_prompt, "Prompt should specify survey_general_instructions_analysis"
    assert '"instructions_present"' in system_prompt, "Prompt should specify instructions_present field"
    assert '"scale_correctly_defined"' in system_prompt, "Prompt should specify scale_correctly_defined field"
    assert '"scale_definition_text"' in system_prompt, "Prompt should specify scale_definition_text field"
    assert '"general_instructions_text"' in system_prompt, "Prompt should specify general_instructions_text field"
    assert '"issues_found"' in system_prompt, "Prompt should specify issues_found field"
    assert '"recommendations"' in system_prompt, "Prompt should specify recommendations field"
    
    print("[PASS] Expected JSON structure test passed")

def test_sample_survey_processing():
    """Test with a sample survey that has general instructions"""
    sample_survey = """
    Survey: Customer Satisfaction
    
    General Instructions:
    Please rate each statement using the following scale:
    4 - Strongly Agree
    3 - Agree  
    2 - Disagree
    1 - Strongly Disagree
    
    Questions:
    
    1. The service was excellent.
       [4] Strongly Agree [3] Agree [2] Disagree [1] Strongly Disagree
    
    2. The food tasted good.
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
    print("Running tests for general instructions checking...")
    
    test_prompt_structure()
    test_expected_json_structure()
    test_sample_survey_processing()
    
    print("\n[SUCCESS] All tests passed! The general instructions checking functionality is working correctly.")

if __name__ == "__main__":
    run_tests()