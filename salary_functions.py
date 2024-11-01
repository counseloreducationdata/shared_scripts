# Module with functions to extract salary information from job postings
# Emilio Lehoucq

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

def find_match_salary(text, type):
    """
    Function to extract salary information from a job posting.

    Input: text (str) - job posting text
    Output (tuple or None): Tuple with the matched salaries and the strings around the first match if found, otherwise None.

    Dependencies: re
    """
    # Check that the input is a string
    if not isinstance(text, str):
        return 'input_is_not_string'

    # Define regex for salary ranges
    # Matches salary ranges such as $30,000 - $40,000
    if type=='range_annual': salary = re.finditer(r'[€£$]\s?\d{1,3}[,.]?\d{3}(?:\.\d{2})?\s?(?:-|–|up to|to|and)\s?[€£$]?\s?\d{1,3}[,.]?\d{3}(?:\.\d{2})?', text.lower())
    # Matches salary ranges such as 30,000 - 40,000
    elif type=='range_annual_no_money_sign': salary = re.finditer(r'\d{2,3}[,.]?\d{3}(?:\.\d{2})?\s?(?:-|–|up to|to|and)\s?\d{2,3}[,.]?\d{3}(?:\.\d{2})?', text.lower())
    # Matches salary ranges such as $30k - $40k
    elif type=='range_annual_k': salary = re.finditer(r'[€£$]\s?\d{1,3}[kK]?\s?(?:-|–|up to|to|and)\s?[€£$]?\s?\d{1,3}[kK]?', text.lower())
    # Matches yearly or monthly salary such as $30,000 or $3,000
    elif type=='annual_or_monthly': salary = re.finditer(r'[€£$]\s?\d{1,3}[,.]?\d{3}(?:\.\d{2})?', text.lower())
    # Matches yearly or monthly salary without money sign such as 30,000 or 3,000
    elif type=='annual_or_monthly_no_money_sign': salary = re.finditer(r'\d{1,3}[,.]\d{3}\.\d{2}', text.lower())
    
    # Create variables to store the salary info
    salary_extracted = []
    salary_string_extracted = []

    # Iterate over potential matches
    for match in salary:
        # Get the start and end index of the match
        start_index = match.start()
        end_index = match.end()
        # Get the matched text
        match_text = match.group().strip()
        # Get characters around the matched text
        match_string = text[start_index-100:end_index+250].replace('\n', ' ').strip()
        # Store the salary info
        salary_extracted.append(match_text)
        salary_string_extracted.append(match_string)

    # If salary info is found, return it wihout duplicates
    if len(salary_extracted) > 0: return list(set(salary_extracted)), salary_string_extracted

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

    # Tests for find_match_salary function
    print("Running tests for find_match_salary function (note: NOT COMPREHENSIVE).")
    # Test 1
    text = 'The salary for this position is $30,000 - $40,000 per year.'
    print("Test 1")
    print("Input text:", text)
    print("Output:", find_match_salary(text, 'range_annual'))
    assert find_match_salary(text, 'range_annual') == (['$30,000 - $40,000'], ['The salary for this position is $30,000 - $40,000 per year.'])
    # Test 2
    text = 'The salary for this position is 30,000 - 40,000 per year.'
    print("Test 2")
    print("Input text:", text)
    print("Output:", find_match_salary(text, 'range_annual_no_money_sign'))
    assert find_match_salary(text, 'range_annual_no_money_sign') == (['30,000 - 40,000'], ['The salary for this position is 30,000 - 40,000 per year.'])
    # Test 3
    text = 'The salary for this position is $30k - $40k per year.'
    print("Test 3")
    print("Input text:", text)
    print("Output:", find_match_salary(text, 'range_annual_k'))
    assert find_match_salary(text, 'range_annual_k') == (['$30k - $40k'], ['The salary for this position is $30k - $40k per year.'])
    # Test 4
    text = 'The salary for this position is $30,000 per year.'
    print("Test 4")
    print("Input text:", text)
    print("Output:", find_match_salary(text, 'annual_or_monthly'))
    assert find_match_salary(text, 'annual_or_monthly') == (['$30,000'], ['The salary for this position is $30,000 per year.'])
    # Test 5
    text = 'The salary for this position is 30,000.00 per year.'
    print("Test 5")
    print("Input text:", text)
    print("Output:", find_match_salary(text, 'annual_or_monthly_no_money_sign'))
    assert find_match_salary(text, 'annual_or_monthly_no_money_sign') == (['30,000.00'], ['The salary for this position is 30,000.00 per year.'])
    # # Test 6
    # text = 'The salary for this position is $10 per hour.'
    # print("Test 6")
    # print("Input text:", text)
    # print("Output:", find_match_salary(text, 'hourly'))
    # assert find_match_salary(text, 'hourly') == (['$10'], ['The salary for this position is $10 per hour.'])
    # # Test 7
    # text = 'The salary for this position is $10 - $20 per hour.'
    # print("Test 7")
    # print("Input text:", text)
    # print("Output:", find_match_salary(text, 'hourly_range'))
    # assert find_match_salary(text, 'hourly_range') == (['$10 - $20'], ['The salary for this position is $10 - $20 per hour.'])
    # Test 8
    text = 'The salary for this position depends on experience.'
    print("Test 8")
    print("Input text:", text)
    print("Output:", find_match_salary(text, 'annual_or_monthly_no_money_sign'))
    assert find_match_salary(text, 'annual_or_monthly_no_money_sign') == None
    # Test 9
    text = 30000
    print("Test 9")
    print("Input text:", text)
    print("Output:", find_match_salary(text, 'annual_or_monthly_no_money_sign'))
    assert find_match_salary(text, 'annual_or_monthly_no_money_sign') == 'input_is_not_string'