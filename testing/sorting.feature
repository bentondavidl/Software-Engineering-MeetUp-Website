Feature: Sorting Events
    In order to better organize events
    As a user
    I want to be able to view events in a sorted order

    Scenario: Sorting events by a certain criteria
        Given we are on the events page, and have a sorting option selected
        When we click the sort button
        Then we should see the events sorted in order based off the sorting option
