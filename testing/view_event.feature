Feature: View an event
    In order to view an event
    As a user or atendee
    I want to be able to see the event details

    Scenario: Navigating to event from homepage
        Given we are on the homepage
        When we click on an event in the public event list
        Then we should be taken to the details of the event
    
    Scenario: Getting event details from event list page
        Given we are on the event list page
        When we click an event
        Then we should be taken to the details of the event

    Scenario: Getting to event from profile page
        Given we are on the profile page
        When we click on an event in the accepted events list
        Then we should be taken to that event's details
    
    Scenario: Getting all details of an event
        Given We are looking at an event
        When we look at the event details
        Then we should see the host, descirption, attendees, picture, location, start and end time
    
        
    