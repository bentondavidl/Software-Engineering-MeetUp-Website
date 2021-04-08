Feature: Login/logout
    In order to see what events I have expressed interest for and to see other events
    As a user
    I want to be able to log in and log out

    Scenario: Log in success
        Given user name and password have been entered correctly in the log in screen
        When I click the log in button
        Then I should be logged in and redirected to the home page
    
    Scenario: Log in failure
        Given user name and password are not entered correctly in the log in screen
        When I click the log in button
        Then I should be told the username and/or password is incorrect

    Scenario: log out
        Given I am logged in
        When I click the log out button from any page
        Then I should be signed out and redirected to the home page
    
    
    
    
    
    