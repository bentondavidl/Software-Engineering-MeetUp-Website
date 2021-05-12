Feature: Event Images
    In order to add an image to my event
    As an event host
    I want to be able add and see an image linked to my event

    Scenario: Adding image from new event screen
        Given we are creating a new event
        When we click on create event
        Then we should see the image on the event page

    Scenario: Adding image from edit event screen
        Given we are the host of the event, and on the edit event page
        When we click the create event button
        then we should see our updated event with an image on it's event page
