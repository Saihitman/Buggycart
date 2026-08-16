from behave import given, when, then
from selenium.webdriver.common.by import By

URL="http://localhost:5000"

@given('I navigate to BuggyCart store')
def step_open_store(context):
    context.driver.get(URL)

@when('I enter username "{user}" and wrong password "{pwd}"')
def step_enter_credentials(context, user, pwd):
    context.driver.find_element(By.ID, "username").send_keys(user)
    context.driver.find_element(By.ID, "password").send_keys(pwd)

@when('I click the login button')
def step_click_login(context):
    context.driver.find_element(By.ID, "loginBtn").click()

@then('I should see an error message "{expected_error}"')
def step_verify_error(context, expected_error):
    actual_error = context.driver.find_element(By.ID, "Invalid Credentials").text
    assert actual_error == expected_error, f"Expected '{expected_error}', but got '{actual_error}'"
