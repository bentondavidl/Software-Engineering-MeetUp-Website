Feature: Create an Event
    In order to share my event with other users,
    As a host
    I want to be able to create an event

    Scenario: Incomplete event creation
        Given not all required fields are filled out in the event creation form
        When I click the create event button
        Then I should be prompted to fill in the required fields
    
    Scenario: Complete event form
        Given all required feilds are filled out
        When I click the create event button
        Then I should be redirected to the event page to review the new event
    
    Scenario: Get to create event
        Given I am on any page in the site
        When I click the create event button in the nav bar
        Then I should be redirected to the create event page
    
    