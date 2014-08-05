           _.====.._
         ,:._       ~-_
             `\        ~-_
               |          `.
             ,/             ~-_
    -..__..-''                 ~~--..__...----...


SURFSTAT
========

Two Click Setup for a Status Webpage.
This web app can report the status of anything, whether it be network servers,
electrical outages, weather on the beach, etc.  Thus, we've defined these as "surfices."
Every surfice has a status (that you create!) and can be updated from the admin side.
"Dings," or issues, can be reported by users and optionally shown on the home page.

Events are stored in the database so that you can track any time the status of a surfice
is updated.

In addition, all your surfices can be categorized under "surfs" so that you have ultimate
control.

Goals
-----

- Have an extensible framework for presenting and reporting statuses
- Be able to plug-in any module to make Surfstat more specific

What We've Done
---------------
- Designed 85% of the templates
- Pull data from an SQLite database
- Write Dings (issues) to the database and update statuses/create events

Programming Goals
-----------------
- Add, update, delete surfs and surfices
- A surfice can only be part of one surf
- We want to be able to report the status (with a color) of any surfice
- Any issues that are reported are able to be viewed both on the admin side and on the frontend
  - Email once a threshold has been reached
- Email to Groups
- Email someone once issues reach a peak set in the admin site
- Unlimited events stored in the database for EVERY status update
  - Still have the ability to edit and delete events
- LDAP login for admin


- Future:
- Maintenance Plugin
  - Ahead of time
  - Start it
  - End it
- Network Plugin
  - Tie in real-time network info (like bandwidth usage, spam filtering, etc.) on homepage

TO DO
=====
UI
--
- ~~Finish templatifying design~~
- Add frontside form checking
- ~~Hit enter for forms to submit~~
- ~~Restrict "What's Happening Lately?" to 2 weeks and up to ~10 entries~~
- Initial setup step-by-step process (and can choose MySQL, SQLite, or PostgreSQL)
- Email to Groups
- ~~Make sure UX is excellent~~
- Choose a surf (or multiple surfs) to show on homepage (admin settings page)
- Update individual surfices in a surf

AJAX
----
- ~~AJAX check if name is already in database when creating/updating a Surf/Surfice/Status~~
- AJAX function to update all AJAX get fields on a page
  - ~~Surfs~~
  - ~~Surfices~~
  - ~~Statuses~~
  - Settings
  - ~~Events~~
  - ~~Dings~~
- ~~Change all AJAX functions to use id rather than name~~
- ~~Deleting a Surf only asks to move surfices to another surf if this surf has surfices.~~
- ~~Add notification system that pops up whenever changes are made~~

Backend
-------
- ~~Deleting a Surf gives you the option to move all containing Surfices to another surfice~~
- ~~Deleting a Surfice also removes all events/dings associated with it~~
- ~~Disable deleting a Surf or Status if this is the last one~~
- ~~Validate email and other info on server side when updating/creating/deleting info~~
- ~~Make checkers for Ding.create()~~
- ~~Flesh out Surf.get_surfs() and all getters to include orderby and other filters (create a generic filter)~~
- ~~When deleting a status, all Surfices associated with it can be given a new status without throwing a new event (and all events associated with the status are either updated or deleted)~~
- ~~Implement admin login~~
- ~~Hook admin into LDAP~~
- Add comments everywhere! Especially HTML, CSS, JavaScript, views.py, urls.py, ajax.py
- Initial setup step-by-step process (and can choose MySQL, SQLite, or PostgreSQL)
- Email to Groups
- Events can be for surfices or surfs
  - ~~Deleting surfs or ~~surfices~~ (done) also deletes the respective events and dings~~

Data
----
- ~~Add generic JSON columns for every data model~~
- ~~One Surfice can be in multiple Surfs (category model)~~
  - ~~A Surfice can have zero Surfs~~
- Set up MySQL in addition to SQLite

Testing
-------
- ~~Make a test deployment server~~
- Test database creation
- Test initial setup

Special thanks to Vada Bennett for assisting with the design.