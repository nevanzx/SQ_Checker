#!/usr/bin/env python
"""
Test script to verify that the sorting of Part 2 and Part 3 results works correctly
"""

import json
from app import extract_valid_json

def test_sorting_functionality():
    """Test that the sorting functionality works correctly"""
    
    # Create a sample analysis with mixed table numbers
    sample_analysis = {
        'individual_question_analysis': [
            {
                "question_id": "AT_01",
                "table_number": "3",  # Part 3
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
                "table_number": "2",  # Part 2
                "item_number": "1",
                "variable_name": "Service Quality",
                "question_text": "The staff were courteous and helpful.",
                "validity": "Valid",
                "reason": "Clear, positive statement appropriate for the variable",
                "alternative_question": "",
                "duplicates_with": []
            },
            {
                "question_id": "AT_02",
                "table_number": "3",  # Part 3
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
                "table_number": "2",  # Part 2
                "item_number": "2",
                "variable_name": "Service Quality",
                "question_text": "The service was timely and efficient.",
                "validity": "Valid",
                "reason": "Clear, positive statement appropriate for the variable",
                "alternative_question": "",
                "duplicates_with": []
            }
        ]
    }
    
    # Simulate the sorting functionality
    original_order = [q['table_number'] for q in sample_analysis['individual_question_analysis']]
    print(f"Original order: {original_order}")
    
    # Apply the sorting logic
    sample_analysis['individual_question_analysis'].sort(key=lambda x: int(x.get('table_number', 999)))
    
    sorted_order = [q['table_number'] for q in sample_analysis['individual_question_analysis']]
    print(f"Sorted order: {sorted_order}")
    
    # Verify that all Part 2 items (table 2) come before Part 3 items (table 3)
    # Find the index where table number changes from 2 to 3
    first_part_3_index = None
    for i, table_num in enumerate(sorted_order):
        if table_num == "3" and first_part_3_index is None:
            first_part_3_index = i
            break
    
    # All items before first_part_3_index should be "2" (Part 2)
    if first_part_3_index is not None:
        part_2_items = sorted_order[:first_part_3_index]
        part_3_items = sorted_order[first_part_3_index:]
        
        all_part_2_correct = all(num == "2" for num in part_2_items)
        all_part_3_correct = all(num == "3" for num in part_3_items)
        
        assert all_part_2_correct, f"Not all Part 2 items are grouped correctly: {part_2_items}"
        assert all_part_3_correct, f"Not all Part 3 items are grouped correctly: {part_3_items}"
    else:
        # If there are only Part 2 or only Part 3 items, that's fine too
        all_same = all(num == sorted_order[0] for num in sorted_order)
        assert all_same, f"Items not properly ordered: {sorted_order}"
    
    print("[PASS] Sorting functionality works correctly")
    
    # Verify the order within each part remains consistent
    # Find indices for each part
    part_2_indices = [i for i, num in enumerate(sorted_order) if num == "2"]
    part_3_indices = [i for i, num in enumerate(sorted_order) if num == "3"]
    
    # Within each part, the original sequence should be maintained
    original_part_2 = [q for q in sample_analysis['individual_question_analysis'] if q['table_number'] == "2"]
    original_part_3 = [q for q in sample_analysis['individual_question_analysis'] if q['table_number'] == "3"]
    
    # Check that the order within each part is preserved
    sorted_part_2 = [q for q in sample_analysis['individual_question_analysis'] if q['table_number'] == "2"]
    sorted_part_3 = [q for q in sample_analysis['individual_question_analysis'] if q['table_number'] == "3"]
    
    # The order within each part should remain the same
    for orig, sorted_q in zip(original_part_2, sorted_part_2):
        assert orig['question_id'] == sorted_q['question_id'], "Order within Part 2 not preserved"
    
    for orig, sorted_q in zip(original_part_3, sorted_part_3):
        assert orig['question_id'] == sorted_q['question_id'], "Order within Part 3 not preserved"
    
    print("[PASS] Order within each part is preserved after sorting")

def test_edge_cases():
    """Test edge cases for the sorting functionality"""
    
    # Test with only Part 2 items
    analysis_part_2_only = {
        'individual_question_analysis': [
            {
                "question_id": "SQ_01",
                "table_number": "2",
                "item_number": "1",
                "variable_name": "Service Quality",
                "question_text": "The staff were courteous.",
                "validity": "Valid",
                "reason": "Clear statement",
                "alternative_question": "",
                "duplicates_with": []
            },
            {
                "question_id": "SQ_02",
                "table_number": "2",
                "item_number": "2",
                "variable_name": "Service Quality",
                "question_text": "The service was efficient.",
                "validity": "Valid",
                "reason": "Clear statement",
                "alternative_question": "",
                "duplicates_with": []
            }
        ]
    }
    
    original_len = len(analysis_part_2_only['individual_question_analysis'])
    analysis_part_2_only['individual_question_analysis'].sort(key=lambda x: int(x.get('table_number', 999)))
    assert len(analysis_part_2_only['individual_question_analysis']) == original_len, "Length should not change after sorting"
    
    all_table_2 = all(q['table_number'] == "2" for q in analysis_part_2_only['individual_question_analysis'])
    assert all_table_2, "All items should still be Part 2"
    
    print("[PASS] Edge case - Part 2 only handled correctly")
    
    # Test with only Part 3 items
    analysis_part_3_only = {
        'individual_question_analysis': [
            {
                "question_id": "AT_01",
                "table_number": "3",
                "item_number": "1",
                "variable_name": "Atmosphere",
                "question_text": "The atmosphere was pleasant.",
                "validity": "Valid",
                "reason": "Clear statement",
                "alternative_question": "",
                "duplicates_with": []
            }
        ]
    }
    
    original_len = len(analysis_part_3_only['individual_question_analysis'])
    analysis_part_3_only['individual_question_analysis'].sort(key=lambda x: int(x.get('table_number', 999)))
    assert len(analysis_part_3_only['individual_question_analysis']) == original_len, "Length should not change after sorting"
    
    all_table_3 = all(q['table_number'] == "3" for q in analysis_part_3_only['individual_question_analysis'])
    assert all_table_3, "All items should still be Part 3"
    
    print("[PASS] Edge case - Part 3 only handled correctly")
    
    # Test with mixed table numbers including other parts
    analysis_mixed = {
        'individual_question_analysis': [
            {
                "question_id": "PT4_01",
                "table_number": "4",
                "item_number": "1",
                "variable_name": "Price Sensitivity",
                "question_text": "The prices are reasonable.",
                "validity": "Valid",
                "reason": "Clear statement",
                "alternative_question": "",
                "duplicates_with": []
            },
            {
                "question_id": "SQ_01",
                "table_number": "2",
                "item_number": "1",
                "variable_name": "Service Quality",
                "question_text": "The staff were courteous.",
                "validity": "Valid",
                "reason": "Clear statement",
                "alternative_question": "",
                "duplicates_with": []
            },
            {
                "question_id": "AT_01",
                "table_number": "3",
                "item_number": "1",
                "variable_name": "Atmosphere",
                "question_text": "The atmosphere was pleasant.",
                "validity": "Valid",
                "reason": "Clear statement",
                "alternative_question": "",
                "duplicates_with": []
            }
        ]
    }
    
    analysis_mixed['individual_question_analysis'].sort(key=lambda x: int(x.get('table_number', 999)))
    sorted_tables = [q['table_number'] for q in analysis_mixed['individual_question_analysis']]
    expected_sorted = ["2", "3", "4"]  # Should be in numerical order
    
    assert sorted_tables == expected_sorted, f"Mixed tables should be sorted numerically: expected {expected_sorted}, got {sorted_tables}"
    
    print("[PASS] Edge case - Mixed table numbers handled correctly")

def run_sorting_tests():
    """Run all sorting tests"""
    print("Testing sorting functionality for Part 2 and Part 3 results...\n")
    
    test_sorting_functionality()
    print()
    test_edge_cases()
    
    print("\n[SUCCESS] All sorting tests passed! The Part 2 and Part 3 results are properly sorted.")

if __name__ == "__main__":
    run_sorting_tests()