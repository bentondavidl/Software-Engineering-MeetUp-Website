Feature: Edit existing event
    In order to update the details for an event
    As a host
    I want to be able to edit an existing event

    Scenario: Get to edit event
        Given I am on an event page and I am the Host
        When I click the edit event button
        Then I should be redirected to the edit event page
    
    Scenario: Update event
        Given I am on the edit event page and have finished my edits
        When I click save changes
        Then I should be redirected to the event page to review the changes
    
    Scenario: Bad event edits
        Given I am on the edit event page and I make the event invalid
        When I click save changes
        Then I am given a warning to fix errors before the changes are accepted
    
    