Feature: iCal Download
    In order to allow users to download events
    As a user
    I want to download and export the iCal representation for an event

    Scenario: Downloading iCal from the event page
        Given we are on the event's page
        When we click the download iCal button
        Then we should see the iCal download in the browser
