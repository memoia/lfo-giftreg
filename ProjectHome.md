Code Sample for LFO, "Sample Project 2: The Gift Registry".

---

Project directions:

Write a web-based application that provides an interface for greedy party throwers and their stingy guests.

Assume there are the following kinds of users:
  * Recipients, who set up Events and receive gifts at an Event
  * Attendees, who give gifts at an Event

Also assume the following relationships:
  * Events
    * have a single Recipient
    * have many Attendees
  * Recipients
    * have a single Event
    * have many Gifts they wish to receive
  * Attendees
    * have multiple Events they may attend
    * may have a Budget for an Event
  * Gifts
    * have a Name
    * are worth some Value

Use Cases:
  1. As a recipient, I should be able to create an Event for which gifts are to be registered.
  1. As a Recipient, I should be able to add and remove Gifts that I would like to receive at my Event.
  1. As a Recipient, I should be able to invite Attendees to my Event.
  1. As an Attendees, I should be able to select at least one gift, but no more than two.
  1. As an Attendees, I should specify my budget for an Event. I should not be able to select Gifts that total more than my Budget for an Event.
  1. As a Recipient, I should only receive a maximum of one of any Gift at an Event.