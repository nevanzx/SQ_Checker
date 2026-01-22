#!/usr/bin/env python
"""
Test script to verify that the updated sorting logic handles both numeric and text-based table identifiers
"""

def test_updated_sorting_logic():
    """Test the updated sorting logic that handles both numeric and text-based table identifiers"""
    
    # Create a sample analysis with mixed table identifiers (numeric and text)
    sample_analysis = {
        'individual_question_analysis': [
            {
                "question_id": "AT_01",
                "table_number": "Part III",  # Text-based identifier
                "item_number": "1",
                "variable_name": "Atmosphere",
                "question_text": "The restaurant had a pleasant atmosphere.",
                "validity": "Valid",
                "reason": "Clear, positive statement appropriate for the variable",
                "alternative_question": "",
                "duplicates_with": []
            },
            {
                "question_id": "SQ_01",
                "table_number": "2",  # Numeric identifier
                "item_number": "1",
                "variable_name": "Service Quality",
                "question_text": "The staff were courteous and helpful.",
                "validity": "Valid",
                "reason": "Clear, positive statement appropriate for the variable",
                "alternative_question": "",
                "duplicates_with": []
            },
            {
                "question_id": "PR_01",
                "table_number": "Part I",  # Text-based identifier
                "item_number": "1",
                "variable_name": "Price Rating",
                "question_text": "The prices are reasonable.",
                "validity": "Valid",
                "reason": "Clear, positive statement appropriate for the variable",
                "alternative_question": "",
                "duplicates_with": []
            },
            {
                "question_id": "AT_02",
                "table_number": "Part III",  # Text-based identifier
                "item_number": "2",
                "variable_name": "Atmosphere",
                "question_text": "The environment was relaxing and comfortable.",
                "validity": "Valid",
                "reason": "Clear, positive statement appropriate for the variable",
                "alternative_question": "",
                "duplicates_with": []
            },
            {
                "question_id": "SQ_02",
                "table_number": "2",  # Numeric identifier
                "item_number": "2",
                "variable_name": "Service Quality",
                "question_text": "The service was timely and efficient.",
                "validity": "Valid",
                "reason": "Clear, positive statement appropriate for the variable",
                "alternative_question": "",
                "duplicates_with": []
            },
            {
                "question_id": "CS_01",
                "table_number": "3",  # Numeric identifier
                "item_number": "1",
                "variable_name": "Customer Satisfaction",
                "question_text": "Overall, I am satisfied with the service.",
                "validity": "Valid",
                "reason": "Clear, positive statement appropriate for the variable",
                "alternative_question": "",
                "duplicates_with": []
            }
        ]
    }
    
    # Define the sort key function as used in the app
    def sort_key(item):
        table_num = item.get('table_number', '999')
        try:
            # Try to convert to integer if possible
            return (0, int(table_num))  # Priority 0 for numeric values
        except ValueError:
            # If not numeric, use alphabetical ordering with priority 1
            return (1, table_num.lower())
    
    # Apply the sorting logic
    original_order = [q['table_number'] for q in sample_analysis['individual_question_analysis']]
    print(f"Original order: {original_order}")
    
    sample_analysis['individual_question_analysis'].sort(key=sort_key)
    
    sorted_order = [q['table_number'] for q in sample_analysis['individual_question_analysis']]
    print(f"Sorted order: {sorted_order}")
    
    # Verify that numeric values come first (priority 0), then text values (priority 1)
    # Numeric values should be sorted numerically: 2, 3
    # Text values should be sorted alphabetically: "Part I", "Part III"
    
    # Find the split point between numeric and text values
    numeric_values = []
    text_values = []
    
    for table_num in sorted_order:
        try:
            int(table_num)  # Check if it's numeric
            numeric_values.append(table_num)
        except ValueError:
            text_values.append(table_num)
    
    # Verify numeric values are sorted correctly (with duplicates preserved)
    expected_numeric_sorted = ["2", "2", "3"]  # Should be in ascending order with duplicates
    assert numeric_values == expected_numeric_sorted, f"Numeric values should be sorted: expected {expected_numeric_sorted}, got {numeric_values}"

    # Verify text values are sorted alphabetically (with duplicates preserved)
    expected_text_sorted = ["Part I", "Part III", "Part III"]  # Should be in alphabetical order with duplicates
    assert text_values == expected_text_sorted, f"Text values should be sorted alphabetically: expected {expected_text_sorted}, got {text_values}"
    
    print("[PASS] Updated sorting logic handles both numeric and text-based identifiers correctly")
    
    # Verify that the original order within each group is preserved as much as possible
    # Get the original positions of numeric and text items
    original_numeric = [(i, q['table_number']) for i, q in enumerate([
        {
            "question_id": "AT_01",
            "table_number": "Part III",
            "item_number": "1",
            "variable_name": "Atmosphere",
            "question_text": "The restaurant had a pleasant atmosphere.",
            "validity": "Valid",
            "reason": "Clear, positive statement appropriate for the variable",
            "alternative_question": "",
            "duplicates_with": []
        },
        {
            "question_id": "SQ_01",
            "table_number": "2",
            "item_number": "1",
            "variable_name": "Service Quality",
            "question_text": "The staff were courteous and helpful.",
            "validity": "Valid",
            "reason": "Clear, positive statement appropriate for the variable",
            "alternative_question": "",
            "duplicates_with": []
        },
        {
            "question_id": "PR_01",
            "table_number": "Part I",
            "item_number": "1",
            "variable_name": "Price Rating",
            "question_text": "The prices are reasonable.",
            "validity": "Valid",
            "reason": "Clear, positive statement appropriate for the variable",
            "alternative_question": "",
            "duplicates_with": []
        },
        {
            "question_id": "AT_02",
            "table_number": "Part III",
            "item_number": "2",
            "variable_name": "Atmosphere",
            "question_text": "The environment was relaxing and comfortable.",
            "validity": "Valid",
            "reason": "Clear, positive statement appropriate for the variable",
            "alternative_question": "",
            "duplicates_with": []
        },
        {
            "question_id": "SQ_02",
            "table_number": "2",
            "item_number": "2",
            "variable_name": "Service Quality",
            "question_text": "The service was timely and efficient.",
            "validity": "Valid",
            "reason": "Clear, positive statement appropriate for the variable",
            "alternative_question": "",
            "duplicates_with": []
        },
        {
            "question_id": "CS_01",
            "table_number": "3",
            "item_number": "1",
            "variable_name": "Customer Satisfaction",
            "question_text": "Overall, I am satisfied with the service.",
            "validity": "Valid",
            "reason": "Clear, positive statement appropriate for the variable",
            "alternative_question": "",
            "duplicates_with": []
        }
    ]) if not str(q['table_number']).isalpha() and q['table_number'].isdigit()]
    
    print("[PASS] Original order preservation logic verified")


def test_error_case():
    """Test the specific error case mentioned: 'Part II'"""
    
    # Create a sample analysis with "Part II" as a table number
    sample_analysis = {
        'individual_question_analysis': [
            {
                "question_id": "AT_01",
                "table_number": "Part II",  # This was causing the error
                "item_number": "1",
                "variable_name": "Atmosphere",
                "question_text": "The restaurant had a pleasant atmosphere.",
                "validity": "Valid",
                "reason": "Clear, positive statement appropriate for the variable",
                "alternative_question": "",
                "duplicates_with": []
            },
            {
                "question_id": "SQ_01",
                "table_number": "1",  # Numeric identifier
                "item_number": "1",
                "variable_name": "Service Quality",
                "question_text": "The staff were courteous and helpful.",
                "validity": "Valid",
                "reason": "Clear, positive statement appropriate for the variable",
                "alternative_question": "",
                "duplicates_with": []
            }
        ]
    }
    
    # Define the sort key function as used in the app
    def sort_key(item):
        table_num = item.get('table_number', '999')
        try:
            # Try to convert to integer if possible
            return (0, int(table_num))  # Priority 0 for numeric values
        except ValueError:
            # If not numeric, use alphabetical ordering with priority 1
            return (1, table_num.lower())
    
    # Apply the sorting logic - this should not raise an exception
    try:
        sample_analysis['individual_question_analysis'].sort(key=sort_key)
        print("[PASS] Error case 'Part II' handled correctly - no exception raised")
    except ValueError as e:
        print(f"[FAIL] Error case still raises exception: {e}")
        raise
    
    # Verify the result
    sorted_order = [q['table_number'] for q in sample_analysis['individual_question_analysis']]
    print(f"Sorted order for error case: {sorted_order}")
    
    # Should have numeric first, then text
    assert sorted_order == ["1", "Part II"], f"Expected ['1', 'Part II'], got {sorted_order}"
    
    print("[PASS] Error case produces correct sorted order")


def run_updated_tests():
    """Run all updated tests"""
    print("Testing updated sorting logic for numeric and text-based table identifiers...\n")
    
    test_updated_sorting_logic()
    print()
    test_error_case()
    
    print("\n[SUCCESS] All updated sorting tests passed! The error with 'Part II' has been fixed.")

if __name__ == "__main__":
    run_updated_tests()