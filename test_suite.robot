*** Settings ***
Documentation    Example Robot Framework test suite using custom logger
Library          robot_logger.py
Resource         keywords.resource

*** Test Cases ***
User Login Test
    [Documentation]    Test user login functionality with custom logging
    [Tags]    login    smoke
    Start Test    User Login Test
    
    Step    Navigate to login page
    Navigate To Login Page
    
    Step    Enter username
    Enter Username    testuser@example.com
    
    Step    Enter password
    Enter Password    password123
    
    Step    Click login button
    Click Login Button
    
    Step    Verify login success
    Verify Login Success
    
    Pass Test    User login completed successfully
    End Test    PASS

Form Validation Test
    [Documentation]    Test form validation with error handling
    [Tags]    validation    forms
    Start Test    Form Validation Test
    
    Step    Navigate to registration page
    Navigate To Registration Page
    
    Step    Fill invalid email
    Fill Email Field    invalid-email
    
    Step    Submit form
    Submit Registration Form
    
    Step    Verify validation error
    Verify Validation Error    Invalid email format
    
    Step    Fill valid email
    Fill Email Field    valid@example.com
    
    Step    Submit form again
    Submit Registration Form
    
    Step    Verify success
    Verify Registration Success
    
    Pass Test    Form validation test completed
    End Test    PASS

API Endpoint Test
    [Documentation]    Test API endpoint functionality
    [Tags]    api    backend
    Start Test    API Endpoint Test
    
    Step    Send GET request to users endpoint
    ${response}=    Get Request    /api/users
    
    Step    Verify response status
    Should Be Equal As Integers    ${response.status_code}    200
    
    Step    Verify response format
    Should Not Be Empty    ${response.json()}
    
    Step    Test error endpoint
    ${error_response}=    Get Request    /api/nonexistent
    
    Step    Verify error response
    Should Be Equal As Integers    ${error_response.status_code}    404
    
    Pass Test    API endpoint test completed
    End Test    PASS

*** Test Cases ***
Failed Test Example
    [Documentation]    Example of a test that fails to show error logging
    [Tags]    example    failure
    Start Test    Failed Test Example
    
    Step    Attempt operation that will fail
    ${result}=    Run Keyword And Return Status    Should Be Equal    hello    goodbye
    
    IF    ${result} == False
        Fail    Expected values to be equal but they were not
        Error    Test failed: hello != goodbye
        End Test    FAIL
    END
