# Survey Quality Checker - Enhanced Analysis Features

## Overview
This enhancement adds comprehensive checking of general instructions and Part 2/3 variable definitions in survey questionnaires, with a focus on validating the Likert scale definition and ensuring proper variable definitions.

## Changes Made

### 1. Updated prompts.py
- Enhanced the system prompt to explicitly check general instructions first
- Added specific instructions to verify the 4-Strongly Agree, 3-Agree, 2-Disagree, 1-Strongly Disagree scale
- Added evaluation of Part 2 and Part 3 for variable definitions only
- Modified the expected JSON structure to include both `survey_general_instructions_analysis` and `survey_parts_analysis`

### 2. Updated app.py
- Modified the analysis structure to include both `survey_general_instructions_analysis` and `survey_parts_analysis`
- Updated the `extract_valid_json` function to better handle the new structures
- Enhanced the DOCX report generation to include both general instructions analysis and survey parts analysis
- Updated error handling to include both analyses even when errors occur

## New JSON Structure
The AI model now returns an enhanced JSON structure that includes:

```json
{
    "survey_general_instructions_analysis": {
        "instructions_present": "true/false",
        "scale_correctly_defined": "true/false",
        "scale_definition_text": "exact text of scale definition if present",
        "general_instructions_text": "full text of general instructions",
        "issues_found": ["list of issues with general instructions if any"],
        "recommendations": ["list of recommendations to fix general instruction issues if any"]
    },
    "survey_parts_analysis": {
        "part_2_has_only_definitions": "true/false",
        "part_3_has_only_definitions": "true/false",
        "part_2_content_summary": "summary of what's in part 2",
        "part_3_content_summary": "summary of what's in part 3",
        "part_2_issues": ["list of issues with part 2 if any"],
        "part_3_issues": ["list of issues with part 3 if any"],
        "part_2_recommendations": ["list of recommendations for part 2 if any"],
        "part_3_recommendations": ["list of recommendations for part 3 if any"]
    },
    "individual_question_analysis": [
        // ... existing question analysis structure
    ]
}
```

## Features Added
1. **General Instructions Validation**: Checks if general instructions are present and properly defined
2. **Scale Verification**: Validates that the 4-3-2-1 Likert scale is correctly defined
3. **Part 2/3 Analysis**: Evaluates if these sections contain only variable definitions
4. **Issue Detection**: Identifies problems with general instructions and section content
5. **Results Sorting**: Organizes results so that all Part 2 items appear first, followed by all Part 3 items
6. **Robust Sorting Logic**: Handles both numeric and text-based table identifiers (fixes "invalid literal for int()" error)
7. **Recommendations**: Provides suggestions to fix various issues
8. **Report Integration**: Includes all analyses in the final DOCX report

## Benefits
- More comprehensive survey quality analysis
- Early detection of scale definition issues
- Validation that Part 2 and Part 3 contain only variable definitions
- Properly sorted results for easier review
- Robust handling of different table identifier formats
- Better guidance for survey creators
- Improved reporting with detailed insights