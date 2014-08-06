           _.====.._
         ,:._       ~-_
             `\        ~-_
               |          `.
             ,/             ~-_
    -..__..-''                 ~~--..__...----...


WHAT'S WHAT for SURFSTAT
========

This is a Django project and thus has quite a few files that may not make sense.
The goal of this doc is to explain those files a bit: to give a run through of what does what.
This isn't an in-depth look at every method, mind you, but after reading this, you'll
understand the flow of the website, so that if/when you decide to edit it, you know where
to look.

To start, we'll look at the core files...the ones in /surfstat/.

/surfstat/wsgi.py
-----------------

Think of this file as the start of life.  Everything begins here when deploying surfstat
to a website (i.e. not using the Django development server on your local computer).
I didn't make any changes to this file. It is completely default from the time you create
a Django project.

Before I jump into urls.py, we're going to look at /surfstat/settings/ since that's really
where things go next.

/surfstat/settings/__init__.py
------------------------------
You might be asking yourself why I'm starting with a Python init file. Normally these are
just there to tell Python that the current directory should be interpreted as Python.
This init file is a bit different, though; it actually includes a statement!

`from asbury import *`

The way settings are set up for Surfstat is a little more modular. Basically, any settings
specific to your current setup are included in `asbury.py` or whatever file you specify in
`__init__.py`

/surfstat/settings/asbury.py (or whatever you specify)
------------------------------------------------------
The first thing asbury.py does is import `base.py`. I'll explain that in a little bit.
`asbury.py` includes settings that are specific to Asbury's setup and thus are not included
on GitHub.  For us, this is where we specify email settings, time zone settings, and LDAP
settings.
A very important thing to understand! Any settings specified in `base.py` are overridden
by this file.  The biggest thing to point out are the `STATIC_ROOT` and `STATIC_URL` settings.
`STATIC_ROOT` is the path on your server to the static folder. In my case, it was
`/home/localadm/public_html/static/`, but it could be anything.  Just remember, this is a
Unix path!

`STATIC_URL` on the other hand is relative to how the web server is set up. For example, 
www.test.com might be in `/home/user/public_html/` on the server.  That means that the root
directory of the website is `/home/user/public_html/`.  If we set `STATIC_ROOT` to be in 
`/home/user/public_html/static/`, the static folder is in the root directory, thus we set
`STATIC_URL` to `/static/`.

Confused yet?  Just think of `STATIC_ROOT` as being for the setting for where all your files
GO on the server and `STATIC_URL` is where the website GETS all the files.

If you're feeling especially curious, you can always check out Django's documentation:
https://docs.djangoproject.com/en/1.4/howto/static-files/#deploying-static-files-in-a-nutshell


/surfstat/settings/base.py
--------------------------
After wsgi.py, this is the second most important file to get the website running. Again,
most of the settings in here are default with a few exceptions: INSTALLED_APPS and the LOGIN/LOGOUT
urls.  Remember that all these settings can be overridden by the local settings in `asbury.py`
or whatever file you specify.

/surfstat/urls.py
-----------------
This file specifies all the base urls. This one is pretty basic since it hands off most of
the work to the Surfice urls file.  What this file does is change the default Django database
management url to /db. It also specifies the urls for login and logout, and the rest it
imports from `surfice.urls`.

/surfstat/surfice.db
--------------------
SQLite file that includes all the data. Everything is stored here, so it's not usually good
to delete it.

--------------------

Now it gets into the nitty-gritty stuff: the /surfice/ folder. This is where the application
resides and where 99% of editing will happen.

/surfice/urls.py
----------------
Since we just mentioned the surfstat.urls file, I thought I'd mentioned the surfice.urls
file next.  This is where all the url dispatching happens.  It is full of url tuples which
have a regular expression in them.  Some pass variables to their respective methods in
`views.py` while some do not.  The name assigned to each url tuple is especially important,
since that is the way we can dynamically retrieve the url to a specific page using the
`reverse()` function.

/surfice/views.py
-----------------
This file defines how everything is shown on the webpage. It calls templates, handles
GET and POST operations, and gets necessary information from the database.  An important
thing to note is that you probably don't want just anyone accessing the admin page, so
we restrict those view methods a decorator.

/surfice/ajax.py
----------------
Making a quick detour here from the order of operations to show you the `ajax.py` file. 
This one is related to the `views.py` file since it uses some of the same code. Basically, 
where `views.py` handles page loads, `ajax.py` handles ajax loads.  This file contains plenty
of getters and setters and miscellaneous methods to handle all the ajax requests that
happen on the front page and in the admin site.

Again, most of these methods are restricted to only those who have permission.

/surfice/models.py
------------------
Ah yes. The models file. This is where the magic happens. The Surfice, Surf, etc. objects
are defined in this file so that we can actually use the application.  The methods to add,
delete, and change these object are all included here. Note that if you change any of the
variables that are included in the object (and thus included in the database), you will
either have to re-create the database or do `./manage.py syncdb` (that one doesn't work all
the time...).  This is the exact reason I created the `data` variable: it can hold miscellaneous
information that I might've forgotten to include.

/surfice/templatetags/*
---------------
Python files that can be included in templates. They allow for functionality such as
slugifying text on the fly or other helpful functions.

/surfice/serializers.py
-----------------------
Serializes each of the models so that they include all the data needed.

---------------
The `/surfice/static` and `/surfice/templates` folders are connected. All the CSS, image, and
JavaScript files linked in the template files are in the static folder. We'll go quickly
through the templates folder and then the static folder.

/surfice/templates/surfice/base.html
----------------------------
`base.html` is the main template for every webpage on Surfstat. It is included in all the
page-specific template files in this same folder.  This file includes the home navigation
and most javascript files that are used on Surfstat.

/surfice/templates/surfice/base_*.html
--------------------------------------
All these templates are included in `views.py` mentioned earlier and add the specific
HTML and Javascript code for that page.  Each block is placed in their respective blocks
in the `base.html` file.

/surfice/templates/surfice/admin_nav.html
-----------------------------------------
A snippet of HTML that is included on all the admin pages for the navigation. Simple
as that.

/surfice/static/surfice/*
-------------------------
In general, these files are included in the templates mentioned earlier.

/surfice/static/surfice/carousel.css
------------------------------------
This is the main CSS file that controls the custom styles we applied to Surfstat.

/surfice/static/surfice/bootstrap*.css
--------------------------------------
The main `bootstrap.min.css` file resets all the styles to almost Bootstrap defaults.
The rest of the Bootstrap files are for various plugins that were used in Surfstat.

/surfice/static/surfice/js/bootstrap*.js
----------------------------------------
The main Javascript file for Bootstrap so that modals and other such interactive elements
work correctly.  All other Bootstrap files are for various addons that improve the
user experience of Surfstat.

/surfice/static/surfice/js/effects.js
-------------------------------------
The majority of this file is fired on DOM load.  If anything visual occurs or if anything
interactive happens, it is included in this file.  Things like modal
boxes are set up in this script.  Note that many of the Bootstrap javascript functions are
fired from HTML; I used the `data-` attributes to connect to those functions.

/surfice/static/surfice/js/io.js
--------------------------------
This file handles all forms that fire from the HTML.  These include both normal and ajax
requests.  When submitting a form, it will also collect miscellaneous data with the right
`data-` attribute into a single input with the name `data`.  `models.js` and `refresh.js`
are directly linked to `io.js`.

/surfice/static/surfice/js/models.js
------------------------------------
This file includes models that are very close to mirroring what are in Python.  While they
may be used more in the future, currently the biggest use of these models is just to
provide a central way to get data from the server via ajax. 

/surfice/static/surfice/js/refresh.js
-------------------------------------
`refresh.js` is an incredibly important file for the admin site.  It provides a central
location for refreshing everything on a single web page via ajax and based on `data-`
attributes set in the HTML.  Each time an ajax form is submitted through `io.js`, the page
is automatically refreshed.  Essentially, it searches through the entire DOM looking for
matching `data-` attributes and when it finds it, this file fires a function for that
specific DOM element with the specific data that was `GET`ted

/surfice/static/surfice/js/validate.js
--------------------------------------
This file provides simple automatic validation for forms.  Currently it only generally
checks surf/surfice/status names and emails for validation.

/surfice/static/surfice/js/utils.js
-----------------------------------
This includes some general utilities that are used semi-extensively throughout Surfstat,
such as `slugify()` and `contains()` methods applied to `String`.

------------------------------

Most of the other folders in the root directory are addons to Django that could've been
installed through pip, but decided to make this application less dependent on server installs.


