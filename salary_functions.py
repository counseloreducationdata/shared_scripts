# Module with functions to extract salary information from job postings
# Emilio Lehoucq
# Script with help of ChatGPT and GitHub Copilot

######################################### Importing libraries #########################################
import re

######################################### Defining functions #########################################

def check_salary(text):
    """
    Function to check if a job posting seems to contain salary information.

    Input: text (str) - job posting text
    Output: info_found (str) or None

    Dependencies: re
    """
    # Check that the input is a string
    if not isinstance(text, str):
        return 'input_is_not_string'
    
    # Lowercase the text
    text = text.lower()
    
    # Check if the text mentions keywords
    if 'salary' in text or 'compensation' in text or 'pay' in text:
        # Pattern for money sign and digits
        pattern = r'[€£$]\s?\d{1,6}'
        # Check if the pattern is found in the text
        flag = re.search(pattern, text)
        # If the pattern is found, return 'money_sign_digits'
        if flag:
            return 'money_sign_digits'
        
        # Pattern for numbers that look like salary
        pattern = r'\b\d{1,3}[,.]?\d{3}\b'
        # Check if the pattern is found in the text
        flag = re.search(pattern, text)
        # If the pattern is found, return 'keyword_numbers'
        if flag:
            return 'keyword_numbers'

if __name__ == '__main__':
    print("Script executed as main program.")

    # Tests for check_salary function
    print("Running tests for check_salary function (note: NOT COMPREHENSIVE).")
    # Test 1
    text = 'The salary for this position is $30,000 - $40,000 per year.'
    print("Test 1")
    print("Input text:", text)
    print("Output:", check_salary(text))
    assert check_salary(text) == 'money_sign_digits'
    # # Test 2
    # text = 'The salary for this position is 30,000 - 40,000 per year.'
    # print("Test 2")
    # print("Input text:", text)
    # print("Output:", check_salary(text))
    # assert check_salary(text) == 'keyword_numbers'
    # Test 3
    text = 'The salary for this position is $30k - $40k per year.'
    print("Test 3")
    print("Input text:", text)
    print("Output:", check_salary(text))
    assert check_salary(text) == 'money_sign_digits'
    # Test 4
    text = 'The salary for this position is $30,000 per year.'
    print("Test 4")
    print("Input text:", text)
    print("Output:", check_salary(text))
    assert check_salary(text) == 'money_sign_digits'
    # # Test 5
    # text = 'The salary for this position is 30,000 per year.'
    # print("Test 5")
    # print("Input text:", text)
    # print("Output:", check_salary(text))
    # assert check_salary(text) == 'keyword_numbers'
    # Test 6
    text = 'The salary for this position is $10 per hour.'
    print("Test 6")
    print("Input text:", text)
    print("Output:", check_salary(text))
    assert check_salary(text) == 'money_sign_digits'
    # Test 7
    text = 'The salary for this position is $10 - $20 per hour.'
    print("Test 7")
    print("Input text:", text)
    print("Output:", check_salary(text))
    assert check_salary(text) == 'money_sign_digits'
    # Test 8
    text = 'The salary for this position is ten per hour.'
    print("Test 8")
    print("Input text:", text)
    print("Output:", check_salary(text))
    assert check_salary(text) == None
    # Test 9
    text = 30000
    print("Test 9")
    print("Input text:", text)
    print("Output:", check_salary(text))
    assert check_salary(text) == 'input_is_not_string'
