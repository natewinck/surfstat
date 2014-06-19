from django.db import models
import time
import datetime

# Create your models here.



# -------------------------------------
# Surf Class
# Group container for a set of Surfices
# -------------------------------------

class Surf(models.Model):
	# Class variables
	name 		= models.CharField(max_length=512, unique=True)
	description = models.TextField()
	
	# Class methods
	def __unicode__(self):
		return self.name
	
	
	# STATIC METHOD
	# get_surfices()
	# 
	# surf_name		-	Required
	#
	# Gets all surfices in a specific surf by name of surf
	# Returns:
	#	False if no surfices are found
	#	An Array of surfices if they are found
	#
	@staticmethod
	def get_surfices(surf_name):
		surfices = False
		try:
			# Can we find a surf with the given name?
			# If we can't, the .get() method raises a DoesNotExist exception.
			# So the .get() method returns one model instance or raises an exception.
			surf = Surf.objects.get(name=surf_name)
		
			# Retrieve all of the associated pages.
			# Note that filter returns >= 1 model instance.
			surfices = Surfice.objects.filter(surf=surf)
		
		except Surf.DoesNotExist:
			# We get here if we didn't find the specified category.
			# Don't do anything - the template displays the "no category" message for us.
			pass
		return surfices
	
	


# -------------------------------------
# Surfice Class
# The main class. Contains information connected to various services
# that you run.  Each has the following class variables
#
# name			Name of the service. Needs to be unique within its
#				group
# group			Which Surf group this belongs to. Defaults to NULL
# description	Description of the service
# timestamp		Set automatically the first time the surfice is created
# -------------------------------------
class Surfice(models.Model):
	# Class variables
	name 		= models.CharField(max_length=512, unique=True)
	surf 		= models.ForeignKey(Surf)
	description = models.TextField()
	
	# Status is part of the model
	status = models.ForeignKey('Status')
	
	def __unicode__(self):
		return self.name
	
	#def __init__(self):
	#	self.name = "Default"
	#	self.description = "Default description"
	#	self.group = Surf()
	
	def set_status(self, status):
		self.status = status


# -----------------------------------------
# Status Class (could be in a separate app)
#
# Dictates the status of a generic object.  It [can optionally]
# connect with the a generic status image class NO IT CAN'T
# 
# CLASS VARIABLES
# name			Name of the status e.g. "Totally axed" or "choppy" or "clean"
# description	Description of the status
#
# CLASS METHODS
######void set_default()		Set this status as the default
# -----------------------------------------
class Status(models.Model):
	# Class variables
	name 		= models.CharField(max_length=512, unique=True)
	description = models.TextField()
	
	def __unicode__(self):
		return self.name

	


# -----------------------------------------
# Ding Class
#
# Any object of type Ding is an issue.  This just captures the
# initial issue and then the closing of the ding (issue).
# Any usage of the ding will either need to be added here or
# or added in a different app
#
# CLASS VARIABLES
# timestamp			timestamp of the original issue
# surfice			which "surfice" is having the issue
# name				Name of the user
# -----------------------------------------
class Ding(models.Model):
	# Class variables
	name		= models.CharField(max_length=512, unique=False)
	timestamp	= models.DateField(auto_now=False, auto_now_add=True)
	surfice		= models.ForeignKey(Surfice)
	email		= models.EmailField()
	description	= models.TextField()
	
	def __unicode__(self):
		return self.name

	

# Includes information from users of services that they submit.
# Includes methods that handle the various tasks related to tickets



# --------------------------------------
# Event Class
#
# A class for recording events of a general object
# and what the current status is.
#
# CLASS VARIABLES
# timestamp			timestamp of the event
# status			Status object
# surfice			id of the service
# description		description of the event
# ---------------------------------------
class Event(models.Model):
	# Class variables
	timestamp	= models.DateField(auto_now=512, auto_now_add=True)
	status		= models.ForeignKey(Status)
	surfice		= models.ForeignKey(Surfice)
	name		= models.CharField(max_length=512, unique=False)
	description	= models.TextField()
	
	def __unicode__(self):
		return self.name
	
	
	# create_event(surfice, status, description)
	def create_event(surfice, status, description):
		# Probably need to check these before setting them
		event = Event()
		
		event.surfice = surfice
		event.status = status
		event.description = description
		
		# Update the current status of the surfice
		# I know this is not right...
		surfice.status = status
		
		event.save()
		
		return True
	
	
	# get_events(...)
	# 
	# All arguments are optional, and only one at a time can be used
	# (other than the start, end variables)
	#
	# Valid arguments:
	# days		int in number of days back from the current day to pull events
	# events	int number of events to pull regardless of date
	# start		timestamp (YYYY-MM-DD) of the start date of events
	# end		timestamp (YYYY-MM-DD) of the end date. Gets events
	#			from before and including this date
	# start, end		if both are set, all events between (inclusive)
	#					will be returned
	# [none]	If no argument is passed, all stored events will be returned
	#
	# returns:
	# 	array of events in reverse chronological order (newest first)
	def get_events(**kwargs):
		
		# Empty array of events
		events = []
		
		# Get all events in the past x days
		if   'days' in kwargs:
			x = kwargs['days']
			start = date.today() - timedelta(x)
			# Equivalent in SQL to SELECT ... WHERE timestamp >= start
			Event.objects.filter(timestamp__gte=start).order_by('-timestamp')
			
		# Get the past x number of events	
		elif 'events' in kwargs:
			x = kwargs['events']
			Event.objects.order_by('-timestamp')[x]
		
		# Get events up to the current date from the start date
		# If end is set, get events between (inclusive) these dates			
		elif 'start' in kwargs:
			start = kwargs['start']
			
			# If end is set, get events up to and including that date
			# Else, just use the current date
			if 'end' in kwargs:
				end = kwargs['end']
				Event.objects.filter(timestamp__gte=start, timestamp__lte=end).order_by('-timestamp')
				
			else:
				end = timestamp.timestamp.now().isoformat()
				Event.objects.filter(timestamp__gte=start).order_by('-timestamp')

		# Get events up to and including the end date
		elif 'end' in kwargs:
			end = kwargs['end']
			Event.objects.filter(timestamp__lte=end).order_by('-timestamp')
			
		# If no argument is given, get all events 
		else:
			events = Event.objects.all().order_by('timestamp')
		
		return events

			

