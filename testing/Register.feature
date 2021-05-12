Feature: Registering
    In order to allow users to make accounts
    As a user
    I want to be able to register for an account to use the site

    Scenario: Registering for an account
        Given we are on the register page, and filled out all the required information
        When we click the sign up button
        Then we should be redirected to the home page, and the login button should say logout
