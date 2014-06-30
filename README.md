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
- - Email once a threshold has been reached
- LDAP login for admin
- Email to Groups
- Email someone once issues reach a peak set in the admin site
- Unlimited events stored in the database for EVERY status update
- - Still have the ability to edit and delete events
- Initial setup
- MySQL support?



- Future:
- Maintenance Plugin
- - Ahead of time
- - Start it
- - End it
- Network Plugin
- - Tie in real-time network info (like bandwidth usage, spam filtering, etc.) on homepage