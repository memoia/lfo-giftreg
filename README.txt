IMM4LFO 2011-09-17
Code Sample for SE Team


INSTALLATION

Hopefully you can just use './manage.py runserver' to try it out.
This is my environment:

Linux 2.6.32:
  python -V			    ==> Python 2.6.6
  '.'.join(map(str,django.VERSION)) ==> '1.2.3.final.0'

Windows XP SP3/Cygwin:
  python -V			    ==> Python 2.6.5
  '.'.join(map(str,django.VERSION)) ==> '1.3.1.final.0'


INITIAL DATA

The gr/fixtures/scenario.json file represents a "clean" scenario.
The private/giftreg.db sqlite database is loaded from it.

Users are: richard@foo.bar, rose@foo.bar, {alex,ann,adam,amy}@foo.bar
All users have "password" (without quotes) as the password.
Recipient users' names begin with R, attendee users' names begin with A.
  Richard invites alex, ann, adam.
  Rose invites ann, amy.
  Ann gets impatient (Rose gift).
  Ann gets boat, rocket (Richard gifts).
  Alex gets airplane (Richard gift).

Super user that can access all features available via:
  /gr/auth/login/imm
Disable it by setting GODMODE = False in settings.py.


COMMENTS

This project implements "Sample Project 2: The Gift Registry"
as defined in "Code Sample Guidelines.pdf" (trac: LFO Common, 
CodeSampleGuideLines) sent to me by Joanna Maulding on 2011-09-14 17:27CDT.
The primary "app" is "gr".

My intention is to learn how to use Django, its ORM, and unittest.

Design choices:

* Make use of Django's authentication system to keep track of users;
  extend the User structure to make distinction between user types
  for this particular app.

* Use the Event to enforce the singular relationship between Recipients
  and Events, so that Recipients can potentially have multiple Events 
  in future if we so decide. Keep gift list separate for same reason.

* Single app; gift registry as a whole could be used as a component in
  larger sites (say, an online store).

I have tried to follow the specification as closely as possible, however,
I think that it limits the usefulness of the app. For next time, I think
it might be nice to:

* Eliminate the distinction between user types, allowing users to be
  both recipients and attendees. Maybe consider an event "host"---a user 
  who "owns" an event, and therefore,

* Allow recipients to host more than one event. The spec seems to imply
  that a recipient may only have one event ever, which seriously reduces
  their greed potential. 

* Introduce models for Venue, Store, and Location. Event would relate
  to Venue, Gift would relate to Store, and Location would relate to both.
  Location might include attributes for mailing address and geocoordinates,
  allowing for quick map-drawing through a public API.

* Clarify whether events are exclusive or if any attendee can choose to
  attend any available event.

Afterwards:

* Most of my time was spent finding out how "it's done" in Django.

* I'm more happy that it works than I am with the code behind it.
  Some blocks are repeated where they don't need to be, but the best
  place to put that repeated logic isn't always obvious. Not sure
  how to write tests for the views, which do most of the work.
  This would be something I'd want to look into in the future.



QUESTIONS

* What is the best way to split models and views up into separate
  files, without having to maintain from...import statements for
  each one in the __init__.py file? 

* Where is it best to place code that constrains how data can be used?
  As methods in a custom model manager? In the view that accesses them?
  In the model itself? (And how would that look for models that need to
  be tightly coupled?)

* Are there best practices for choosing field types, beyond minimal
  size? i.e., can I trust the ManyToMany type will work as efficiently
  as if I implemented it "manually" using just ForeignKey types?

* Is there a way to see the SQL generated by the ORM for various queries?






