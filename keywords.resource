*** Settings ***
Documentation    Resource file with custom keywords that integrate with the logger
Library          robot_logger.py
Library          SeleniumLibrary
Library          RequestsLibrary

*** Keywords ***
Navigate To Login Page
    [Documentation]    Navigate to the login page
    Info    Opening browser and navigating to login page
    Open Browser    https://example.com/login    chrome
    Wait Until Page Contains Element    id:username    timeout=10
    Pass Test    Successfully navigated to login page

Enter Username
    [Arguments]    ${username}
    [Documentation]    Enter username in the login form
    Info    Entering username: ${username}
    Input Text    id:username    ${username}
    Pass Test    Username entered successfully

Enter Password
    [Arguments]    ${password}
    [Documentation]    Enter password in the login form
    Info    Entering password (masked for security)
    Input Text    id:password    ${password}
    Pass Test    Password entered successfully

Click Login Button
    [Documentation]    Click the login button
    Info    Clicking login button
    Click Button    id:login-button
    Wait Until Page Contains Element    id:dashboard    timeout=10
    Pass Test    Login button clicked successfully

Verify Login Success
    [Documentation]    Verify that login was successful
    Info    Verifying login success
    Element Should Be Visible    id:dashboard
    Element Should Contain    id:user-welcome    Welcome
    Pass Test    Login verification successful

Navigate To Registration Page
    [Documentation]    Navigate to the registration page
    Info    Navigating to registration page
    Go To    https://example.com/register
    Wait Until Page Contains Element    id:email    timeout=10
    Pass Test    Successfully navigated to registration page

Fill Email Field
    [Arguments]    ${email}
    [Documentation]    Fill the email field with the provided email
    Info    Filling email field with: ${email}
    Input Text    id:email    ${email}
    Pass Test    Email field filled successfully

Submit Registration Form
    [Documentation]    Submit the registration form
    Info    Submitting registration form
    Click Button    id:submit-button
    Sleep    2s    # Wait for form processing
    Pass Test    Registration form submitted

Verify Validation Error
    [Arguments]    ${expected_error}
    [Documentation]    Verify that validation error message is displayed
    Info    Verifying validation error: ${expected_error}
    Element Should Be Visible    id:error-message
    Element Should Contain    id:error-message    ${expected_error}
    Pass Test    Validation error verified successfully

Verify Registration Success
    [Documentation]    Verify that registration was successful
    Info    Verifying registration success
    Element Should Be Visible    id:success-message
    Element Should Contain    id:success-message    Registration successful
    Pass Test    Registration success verified

Get Request
    [Arguments]    ${endpoint}
    [Documentation]    Send GET request to specified endpoint
    Info    Sending GET request to: ${endpoint}
    ${response}=    RequestsLibrary.Get    ${endpoint}
    Info    Response status: ${response.status_code}
    Pass Test    GET request completed
    [Return]    ${response}

Setup API Session
    [Documentation]    Setup API session for testing
    Info    Setting up API session
    Create Session    api    https://api.example.com
    Pass Test    API session setup completed

Teardown API Session
    [Documentation]    Clean up API session
    Info    Cleaning up API session
    Delete All Sessions
    Pass Test    API session cleanup completed

Setup Test Environment
    [Documentation]    Setup test environment before running tests
    Info    Setting up test environment
    # Add any setup logic here
    Pass Test    Test environment setup completed

Teardown Test Environment
    [Documentation]    Clean up test environment after tests
    Info    Cleaning up test environment
    Close All Browsers
    # Add any cleanup logic here
    Pass Test    Test environment cleanup completed

Handle Test Failure
    [Arguments]    ${error_message}
    [Documentation]    Handle test failure with proper logging
    Error    Test failed: ${error_message}
    CustomLogger.Fail    ${error_message}
    Take Screenshot    filename=failure_${TEST_NAME}.png
    Info    Screenshot saved for debugging

Assert Element Contains Text
    [Arguments]    ${locator}    ${expected_text}
    [Documentation]    Assert that element contains expected text
    Info    Verifying element ${locator} contains text: ${expected_text}
    Element Should Contain    ${locator}    ${expected_text}
    Pass Test    Element text verification passed

Wait And Click Element
    [Arguments]    ${locator}    ${timeout}=10s
    [Documentation]    Wait for element and then click it
    Info    Waiting for element ${locator} and clicking it
    Wait Until Element Is Visible    ${locator}    timeout=${timeout}
    Click Element    ${locator}
    Pass Test    Element clicked successfully
