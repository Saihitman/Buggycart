Feature: BuggyCart Functional Testing

  Scenario: Verify invalid password rejects login
    Given I navigate to BuggyCart store
    When I enter username "user" and wrong password "wrongpassword"
    And I click the login button
    Then I should see an error message "Invalid Credentials"