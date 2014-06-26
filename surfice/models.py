from django.db import models
from datetime import date, timedelta


# -------------------------------------
# Surf Class
#
# Group container for a set of Surfices
#
# CLASS VARIABLES
# name			Name of the Surf
# description	Description of the Surf
#
# METHODS
# String		__unicode__(self)
# *Surfice 		get_surfices(self)
# Surf			get_surf(name)
# Surf			create_surf(name, description)
# void			delete_surf(self)
# bool			save_surf(self)
# bool			is_saved(name)
#
# NEED TO DO
def NEED_TO_DO():
	pass
# get_surfs
# set_name
# set_description
# -------------------------------------
class Surf(models.Model):
	# Class variables
	name 		= models.CharField(max_length=512, unique=True)
	description = models.TextField()
	
	# Class methods
	def __unicode__(self):
		return self.name
	
	
	# -------------------------------------
	# get_surfices(self)			
	#
	# Gets all surfices in the current surf object
	#
	# RETURNS
	# False if no surfices are found
	# An Array of surfices if they are found
	# -------------------------------------
	def get_surfices(self):
		try:
			# Can we find a surf with the given name?
			# If we can't, the .get() method raises a DoesNotExist exception.
			# So the .get() method returns one model instance or raises an exception.
			#surf = Surf.objects.get(name=surf_name)
		
			# Retrieve all of the associated pages.
			# Note that filter returns >= 1 model instance.
			surfices = Surfice.objects.filter(surf=self)
		
		except Surf.DoesNotExist:
			# We get here if we didn't find the specified category.
			# Don't do anything - the template displays the "no category" message for us.
			surfices = None
			pass
		return surfices
	
	# --------------------------
	# @staticmethod get_surf(name)
	#
	# Get a Surf object by name from the database
	#
	# INPUT
	# name			The name of the Surf object
	#
	# RETURNS
	# A Surf object
	# null if no object by name
	# ---------------------------
	@staticmethod
	def get_surf(name):
		try:
			surf = Surf.objects.get(name=name)
		except Surf.DoesNotExist:
			surf = None
			pass
		return surf
		
	# -------------------------------------
	# @staticmethod create_surf(name, description)
	#
	# Creates a Surf object in the database defined by the given name and description
	# 
	# INPUT
	# name (required)			A string that gives the name of the surf
	# description (optional)	A string that describes the surf
	#
	# RETURNS
	# The created surf
	# -------------------------------------
	@staticmethod
	def create_surf(name, description=''):
		surf = None
		
		# Check to make sure another Surf object with the same name isn't
		# already in the database
		if not Surf.is_saved(name):
			# Create the Surf object
			surf = Surf()
			
			# Set the surf attributes
			surf.name = name
			surf.description = description
			
			# Save the surf in the database
			surf.save()
		
		# Return the created surf
		return surf
	
	# -------------------------------------
	# delete_surf(self)
	# 
	# Deletes this surf from the database
	# -------------------------------------
	def delete_surf(self):
		# Check to make sure the Surf object is in the database first
		try:
			if Surf.objects.filter(pk=self.id).count() != 0:
				self.delete()
		except Surf.DoesNotExist:
			pass
	
	# -------------------------------------
	# save_surf(self)
	#
	# Saves a NEW Surf object to the database. If a Surf with the same name
	# already exists, nothing happens.
	# 
	# RETURNS
	# True if saved
	# False if not
	# -------------------------------------
	def save_surf(self):
		# Check to see if Surf object is already in database. Don't do anything if so
		if Surf.is_saved(self.name):
			# Do nothing
			flag = False
		else:
			self.save()
			flag = True
		
		return flag
	
	# -------------------------------------
	# @staticmethod is_saved(name)
	# 
	# Checks to see if Surf object is already in database.
	# 
	# INPUT
	# name			Name of the Surf object
	# 
	# RETURNS
	# True if Surf object is in database
	# False if Surf object is not in database
	# -------------------------------------
	@staticmethod
	def is_saved(name):
		if Surf.objects.filter(name=name).count() == 0:
			exists = False
		else:
			exists = True
			
		return exists


# -------------------------------------
# Surfice Class
# The main class. Contains information connected to various services
# that you run.  Each has the following class variables
#
# CLASS VARIABLES
# name			Name of the service. Needs to be unique within its
#				group
# surf			Which Surf group this belongs to. Defaults to NULL
# description	Description of the service
# status		Status of the Surfice
#
# METHODS
# String			__unicode__(self)
# Surfice			get_surfice(name)
# *Surfice			get_surfices(...)
# Status			get_status(self)
# void				set_status(self, status, description)
# *Event			get_events(self, ...)
# void				set_surf(self, surf)
# void				set_description(self, description)
# bool				set_name(self, name)
# Surfice			create_surfice(name, surf, description)
# void				delete_surfice(self)
# bool				save_surfice(self)
# bool				is_saved(name)
# 
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
	
	
	# -------------------------------------
	# get_surfice(name)
	# 
	# Gets the surfice with the define name
	# 
	# INPUT
	# name			The name of the surfice
	#
	# RETURNS
	# A surfice object
	# -------------------------------------
	@staticmethod
	def get_surfice(name='', id=''):
		surfice = None
		if name != '':
			try:
				surfice = Surfice.objects.get(name=name)
			
			except Surfice.DoesNotExist:
				pass
		elif id != '':
			try:
				surfice = Surfice.objects.get(id=id)
			
			except Surfice.DoesNotExist:
				pass
		return surfice
	
	# -------------------------------------
	# get_surfices(...)
	#
	# Gets surfices based on the arguments provided.
	# All arguments are optional. If no arguments are provided,
	# this function gets all the surfices stored in the database
	#
	# surf			Get all surfices belonging to a Surf object
	# name			Get all surfices that CONTAIN this name
	# [both]		If both surf and name are set, get all Surfices that belong
	#				to the Surf object and that contain this name
	#
	# RETURNS
	# An array of found Surfice objects
	# -------------------------------------
	@staticmethod
	def get_surfices(surf=None, name=None):
		
		try:
			
			# If both surf and name are set, find all objects with that Surf
			# and contain the name
			if surf != None and name != None:
				surfices = Surfice.objects.filter(surf=surf.id, name__contains=name)
			
			# If surf is set, find all Surfice objects with that Surf
			elif surf != None:
				# CHECK TO SEE IF THIS IS REAL SURF OBJECT
				surfices = Surfice.objects.filter(surf=surf)
				
			# If name is set, find all Surfices that contain that name
			elif name != None:
				surfices = Surfice.objects.filter(name__contains=name)
			
			# If nothing is set, find all Surfices
			else:
				surfices = Surfice.objects.all()
		
		except Surfice.DoesNotExist:
			# If no Surfices are found, set it to an empty array
			surfices = []
			pass
		
		return surfices
	
	
	# -------------------------------------
	# get_status(self)
	# 
	# Get the status of this Surfice object
	# 
	# RETURNS
	# A status object
	# -------------------------------------
	def get_status(self):
		return self.status
	
	
	# -------------------------------------
	# set_status(self, status)
	# 
	# Sets the status of a surfice object with a status object
	#
	# INPUT
	# self						implicitly set
	# status					a Status object
	# description (optional)	If set (even to a blank string), create an
	#							event along with the status
	# -------------------------------------
	def set_status(self, status, description=False):
		
		# If we want to create an event along with updating the status,
		# do it here.
		if description != False:
			Event.create_event(self, status, description)
		
		self.status = status
		self.save()
	
	# -------------------------------------
	# get_events(self, **kwargs)
	# 
	# Gets the events for this specific Surfice object
	# Shortcut method to the Event.get_events() method
	# 
	# INPUT
	# [Same input variables as Event.get_events()]
	# 
	# RETURNS
	# An array of events
	# -------------------------------------
	def get_events(self, **kwargs):
		# NEED TO WRITE
		events = []
		events = Event.objects.filter(surfice=self.id) #NOT SURE IF THIS WORKS OR NOT
		return events
	
	# -------------------------------------
	# set_surf(self, surf)
	# 
	# Sets the surf of the surfice and saves it to the database
	# 
	# INPUT
	# surf			The surf object that this surfice will be set to
	#
	# -------------------------------------
	def set_surf(self, surf):
		# CHECK IF surf IS SURF OBJECT
		self.surf = surf
		
		# Save surfice object to database
		self.save()
	
	# -------------------------------------
	# set_description(self, description)
	#
	# Sets the description of the surfice and saves it to the database
	#
	# INPUT
	# description			The new description of the surfice object
	# -------------------------------------
	def set_description(self, description):
		# CHECK IF surf IS SURF OBJECT
		self.description = description
		self.save()
	
	# -------------------------------------
	# set_name(self, name)
	#
	# Sets the name of the surfice to a new unique name
	#
	# INPUT
	# name			The new name of the surfice object
	#
	# RETURNS
	# True if set worked
	# False if failed due to name already existing
	# -------------------------------------
	def set_name(self, name):
		code = False
		
		# If you aren't changing the name, don't change it!
		if name == self.name:
			code = False
		
		# Check if new name already exists in database
		# If new name doesn't exist, set this object to that name	
		elif Surfice.objects.filter(name='name').count() == 0:
			self.name = name
			self.save()
			code = True
		return code
	
	# -------------------------------------
	# @staticmethod create_surfice(name, surf, description)
	# 
	# Create a new Surfice object and store it in the database
	# 
	# INPUT
	# name						Name of the Surfice
	# surf						Surf object that this Surfice belongs to
	# description (optional)	Description of the Surfice
	# 
	# RETURNS
	# The created Surfice object
	# -------------------------------------
	@staticmethod
	def create_surfice(name, surf, status, description=''):
		surfice = None
		
		# Check to make sure a Surfice object with the same name
		# isn't already in the database.
		if Surfice.objects.filter(name=name).count() == 0:
			# Create the Surfice object
			surfice = Surfice()
			
			# Set the Surfice class variables
			surfice.name = name
			surfice.surf = surf # I NEED TO CHECK IF THE SURF EXISTS FIRST
			surfice.description = description
			surfice.status = status
			
			# Save the Status object to the database
			surfice.save()
		
		return surfice
		
	
	# -------------------------------------
	# delete_surfice(self)
	# 
	# Deletes this surfice from the database
	# -------------------------------------
	def delete_surfice(self):
		self.delete()
	
	
	# -------------------------------------
	# save_surfice(self)
	#
	# Saves a NEW Surfice object to the database. If a Surfice with the same name
	# already exists, nothing happens.
	#
	# RETURNS
	# True if it saved
	# False if it didn't
	# -------------------------------------
	def save_surfice(self):
		# Check to see if Surfice object is already in database. Don't do anything if so
		if Surfice.is_saved(self.name):
			# Do nothing
			flag = False
		else:
			self.save()
			flag = True
		
		return flag
	
	# -------------------------------------
	# @staticmethod is_saved(name)
	# 
	# Checks to see if Surfice object is already in database.
	# 
	# INPUT
	# name			Name of the Surfice object
	# 
	# RETURNS
	# True if Surfice object is in database
	# False if Surfice object is not in database
	# -------------------------------------
	@staticmethod
	def is_saved(name):
		if Surfice.objects.filter(name=name).count() == 0:
			exists = False
		else:
			exists = True
			
		return exists

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
# METHODS
# 
# Status		create_status(name, description)
# void			delete_status()
######void set_default()		Set this status as the default
# -----------------------------------------
class Status(models.Model):
	# Class variables
	name 		= models.CharField(max_length=512, unique=True)
	description = models.TextField()
	
	def __unicode__(self):
		return self.name
	
	
	# -------------------------------------
	# @staticmethod get_status(name)
	# 
	# Gets a status object by name.
	#
	# INPUT
	# name			The name of the status
	#
	# RETURNS
	# The status object
	# -------------------------------------
	@staticmethod
	def get_status(name='', id=''):
		status = None
		
		if name != '':
			try:
				status = Status.objects.get(name=name)
			except:
				pass
		elif id != '':
			try:
				status = Status.objects.get(id=id)
			except:
				pass
		
		return status
	
	
	
	# -------------------------------------
	# @staticmethod get_statuses()
	# 
	# Gets a list of all the statuses
	#
	# RETURNS
	# The an array of statuses
	# -------------------------------------
	@staticmethod
	def get_statuses():
		try:
			statuses = Status.objects.all()
		except:
			statuses = []
			pass
		return statuses
	
	
	
	# -------------------------------------
	# @staticmethod create_status(name, description)
	#
	# Create a new status with name and optional description
	#
	# INPUT
	# name						Name of the status
	# description (optional)	Description of the status
	#
	# RETURNS
	# The created Status object
	# -------------------------------------
	@staticmethod
	def create_status(name, description=''):
		status = None
		
		# Check to make sure a Status object with the same name
		# isn't already in the database.
		if Status.objects.filter(name=name).count() == 0:
			# Create the Status object
			status = Status()
			
			# Set the Status class variables
			status.name = name
			status.description = description
			
			# Save the Status object to the database
			status.save()
		
		return status
	
	# -------------------------------------
	# delete_status(self)
	# 
	# Deletes this status from the database
	# -------------------------------------
	def delete_status(self):
		self.delete()
	
	# -------------------------------------
	# @staticmethod is_saved(name)
	# 
	# Checks to see if Surf object is already in database.
	# 
	# INPUT
	# name			Name of the Status object
	# 
	# RETURNS
	# True if Status object is in database
	# False if Status object is not in database
	# -------------------------------------
	@staticmethod
	def is_saved(name):
		if Status.objects.filter(name=name).count() == 0:
			exists = False
		else:
			exists = True
			
		return exists
	


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
# status			Status object that the user is reporting
# NEED TO ADD RESOLVED FIELD
# -----------------------------------------
class Ding(models.Model):
	# Class variables
	timestamp	= models.DateTimeField(auto_now=False, auto_now_add=True)
	surfice		= models.ForeignKey(Surfice)
	status		= models.ForeignKey(Status)
	email		= models.EmailField()
	description	= models.TextField()
	
	def __unicode__(self):
		return self.status.name
	
	# -------------------------------------
	# @staticmethod create_ding(surfice, status, email, description)
	# 
	# Creates an event for the set surfice. The surfice's status is also updated
	#
	# INPUT
	# surfice					The surfice object that has a ding
	# status					The reported status of the surfice
	# description (optional)	Description of the event
	# email						The email address of the person who submitted the ding
	#
	# RETURNS
	# The created ding
	# -------------------------------------
	@staticmethod
	def create_ding(surfice, status, email, description=''):
		# Create the Ding object
		ding = Ding()
		
		# Assign the attributes to the Ding object SHOULD CHECK THESE FIRST!
		ding.surfice = surfice
		ding.status = status
		ding.email = email
		ding.description = description
		
		# Save the Ding object to the database
		ding.save()
		
		return ding
	
	
	# Flesh this out...just temporary
	@staticmethod
	def get_dings():
		return Ding.objects.all()



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
	timestamp	= models.DateTimeField(auto_now=512, auto_now_add=True)
	status		= models.ForeignKey(Status)
	surfice		= models.ForeignKey(Surfice)
	description	= models.TextField()
	
	def __unicode__(self):
		return self.status.name
	
	# -------------------------------------
	# @staticmethod create_event(surfice, status, description)
	# 
	# Creates an event for the set surfice. The surfice's status is also updated
	#
	# INPUT
	# surfice					The surfice object that has an event
	# status					The new status of the surfice
	# description (optional)	Description of the event
	#
	# RETURNS
	# The created event
	# -------------------------------------
	@staticmethod
	def create_event(surfice, status, description=''):
		# Probably need to check these before setting them
		event = Event()
		
		# Set the event attributes
		event.surfice = surfice
		event.status = status
		event.description = description
		
		# Update the current status of the surfice
		# BAD MODEL: COMMENTING OUT
		# surfice.set_status(status) ######
		
		# Save the event in the database
		event.save()
		
		return event
	
	
	# -------------------------------------
	# @staticmethod get_events(...)
	# 
	# Gets events in reverse chronological order (newest first) based on the arguments
	# All arguments are optional, and only one at a time can be used
	# (other than the start, end variables)
	#
	# INPUT
	# days		int in number of days back from the current day to pull events
	# events	int number of events to pull regardless of date
	# start		timestamp (YYYY-MM-DD) of the start date of events
	# end		timestamp (YYYY-MM-DD) of the end date. Gets events
	#			from before and including this date
	# start, end		if both are set, all events between (inclusive)
	#					will be returned
	# [none]	If no argument is passed, all stored events will be returned
	#
	# RETURNS
	# Array of events in reverse chronological order (newest first)
	# -------------------------------------
	@staticmethod
	def get_events(**kwargs):
		
		# Empty array of events
		events = []
		
		# Get all events in the past x days
		if   'days' in kwargs:
			x = kwargs['days']
			start = date.today() - timedelta(x)
			# Equivalent in SQL to SELECT ... WHERE timestamp >= start
			events = Event.objects.filter(timestamp__gte=start).order_by('-timestamp', '-id')
			
		# Get the past x number of events	
		elif 'events' in kwargs:
			x = kwargs['events']
			events = Event.objects.all().order_by('-timestamp', '-id')[:x]
		
		# Get events up to the current date from the start date
		# If end is set, get events between (inclusive) these dates			
		elif 'start' in kwargs:
			start = kwargs['start']
			
			# If end is set, get events up to and including that date
			# Else, just use the current date
			if 'end' in kwargs:
				end = kwargs['end']
				events = Event.objects.filter(timestamp__gte=start, timestamp__lte=end).order_by('-timestamp', '-id')
				
			else:
				end = date.today()
				events = Event.objects.filter(timestamp__gte=start).order_by('-timestamp', '-id')

		# Get events up to and including the end date
		elif 'end' in kwargs:
			end = kwargs['end']
			events = Event.objects.filter(timestamp__lte=end).order_by('-timestamp', '-id')
			
		# If no argument is given, get all events 
		else:
			events = Event.objects.all().order_by('-timestamp', '-id')
			
		
		return events

			

