Feature: RSVP for an event
    In order to indicate that I am interested in going to an event,
    As a attendee
    I want to be able to RSVP

    Scenario: RSVP on event page
        Given I am on an event page
        When I click the RSVP button
        Then I should be marked as attending and the page should refresh
    
    Scenario: RSVP on home page
        Given I am on the homepage and looking at the list of published events
        When I click the join event (plus) button
        Then I should be marked as attending
    
    