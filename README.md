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