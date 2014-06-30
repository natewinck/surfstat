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
# Surf			create(name, description)
# void			delete(self, *args, **kwargs)
# Surf			get_surf(name, id)
# *Surf			get_surfs(name)
# *Surfice 		get_surfices(self, name)
# bool			set_name(self, name)
# void			set_description(self, description)
# bool			save_new(self, *args, **kwargs)
# bool			is_saved(name)
#
# -------------------------------------
class Surf(models.Model):
	# Class variables
	name 		= models.CharField(max_length=512, unique=True)
	description = models.TextField()
	
	# Class methods
	def __unicode__(self):
		return self.name
	
	# -------------------------------------
	# @staticmethod create(name, description)
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
	def create(name, description=''):
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
	# delete(self, *args, **kwargs)
	#
	# INPUT
	# args, kwargs			Only for extension of built-in delete() function
	# 
	# Deletes this surf from the database
	# -------------------------------------
	def delete(self, *args, **kwargs):
		# Check to make sure the Surf object is in the database first
		try:
			if Surf.objects.filter(pk=self.id).count() != 0:
				# Call the real delete() function
				super(Surf, self).delete(*args, **kwargs)
		except Surf.DoesNotExist:
			pass
	
	# --------------------------
	# @staticmethod get_surf(name)
	#
	# Get a Surf object by name OR id from the database
	#
	# INPUT
	# name			The name of the Surf object
	# id			The id of the Surf object
	#
	# RETURNS
	# A Surf object
	# None if no object found
	# ---------------------------
	@staticmethod
	def get_surf(name=None, id=None):
		surf = None
		
		if name != None:
			try:
				surf = Surf.objects.get(name__iexact=name)
			except Surf.DoesNotExist:
				pass

		elif id != None:
			try:
				surf = Surf.objects.get(id=id)
			except Surf.DoesNotExist:
				pass


		return surf
	
	# --------------------------
	# @staticmethod get_surfs() ###########
	#
	# Get Surf objects that contain a name.  If no name is given, all Surfs are returned
	#
	# INPUT
	# name			The name of Surf to search for
	# [none]		Get all Surfs
	#
	# RETURNS
	# An array of Surf objects
	# Empty array if none found
	# ---------------------------
	@staticmethod
	def get_surfs(name=None):
		surfs = []
		
		try:
			# If name parameter is set, find all Surfs that contain that name
			if name != None:
				surfs = Surf.objects.filter(name__icontains=name)

			# If no params are passed, get all the Surfs in the database
			else:
				surfs = Surf.objects.all()
		
		except Surf.DoesNotExist:
			pass
		
		return surfs
	
	# -------------------------------------
	# get_surfices(self)			
	#
	# Gets all surfices in the current surf object.
	# Optionally include a name to filter by surfices that contain the name
	#
	# INPUT
	# name (optional)		Filter surfices to find all that contain name (case insensitive)
	#
	# RETURNS
	# False if no surfices are found
	# An Array of surfices if they are found
	# -------------------------------------
	def get_surfices(self, name=None):
		try:
			# Find all Surfice objects that are in this surf
			# and that also contain the name param
			if name != None:
				surfices = Surfice.objects.filter(surf=self, name__icontains=name)
			
			# If name is not set, get all Surfices under this Surf
			else:
				surfices = Surfice.objects.filter(surf=self)
		
		except Surfice.DoesNotExist:
			# We get here if we didn't find the specified category.
			# Don't do anything - the template displays the "no category" message for us.
			surfices = None
			pass
		
		return surfices
	
	# -------------------------------------
	# set_name(self, name)
	#
	# Sets the name of the surf to a new unique name and saves it to the database
	#
	# INPUT
	# name			The new name of the surf object
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
		elif Surf.objects.filter(name__iexact='name').count() == 0:
			self.name = name
			self.save()
			code = True
		return code
	
	# -------------------------------------
	# set_description(self, description)
	#
	# Sets the description of the surf and saves it to the database
	#
	# INPUT
	# description			The new description of the surf object
	# -------------------------------------
	def set_description(self, description):
		# Set this description to the new one
		self.description = description
		
		# Save this surf to the database
		self.save()
	
	# -------------------------------------
	# save_new(self, *args, **kwargs)
	#
	# Saves a NEW Surf object to the database. If a Surf with the same name
	# already exists, nothing happens.
	#
	# INPUT
	# args, kwargs		Only for future extension of the save() function
	# 
	# RETURNS
	# True if saved
	# False if not
	# -------------------------------------
	def save_new(self, *args, **kwargs):
		# Check to see if Surf object is already in database. Don't do anything if so
		if Surf.is_saved(self.name):
			# Do nothing
			flag = False
		else:
			# Call the real save() method
			super(Surf, self).save(*args, **kwargs)
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
		if Surf.objects.filter(name__iexact=name).count() == 0:
			exists = False
		else:
			exists = True
			
		return exists


# -------------------------------------
# Surfice Class
# The main class. Contains information connected to various services
# that you run.  Each has the following class variables and methods
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
# Surfice			create(name, surf, description)
# void				delete(self, *args, **kwargs)
# Surfice			get_surfice(name, id)
# *Surfice			get_surfices(...)
# Status			get_status(self)
# *Event			get_events(self, ...)
# bool				set_name(self, name)
# void				set_surf(self, surf)
# void				set_description(self, description)
# void				set_status(self, status, description)
# bool				save_new(self, *args, **kwargs)
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
	# @staticmethod create(name, surf, description)
	# 
	# Create a new Surfice object and store it in the database
	# 
	# INPUT
	# name						Name of the Surfice
	# surf						Surf object that this Surfice belongs to
	# status					Status object that Surfice has
	# description (optional)	Description of the Surfice
	# 
	# RETURNS
	# The created Surfice object
	# -------------------------------------
	@staticmethod
	def create(name, surf, status, description=''):
		surfice = None
		
		# Check to make sure a Surfice object with the same name
		# isn't already in the database.
		if Surfice.objects.filter(name__iexact=name).count() == 0:
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
	# delete(self, *args, **kwargs)
	#
	# INPUT
	# args, kwargs		Only for extension of the built-in function
	# 
	# Deletes this surfice from the database
	# -------------------------------------
	def delete(self, *args, **kwargs):
		# Call the real delete() function
		super(Surfice, self).delete(*args, **kwargs)
	
	# -------------------------------------
	# get_surfice(name, id)
	# 
	# Gets the surfice with the defined name OR id
	# 
	# INPUT
	# name			The name of the surfice
	# id			id of the surfice
	#
	# RETURNS
	# A surfice object
	# None if no surfice found
	# -------------------------------------
	@staticmethod
	def get_surfice(name=None, id=None):
		surfice = None
		try:
			# If name is set, find the Surfice whose name matches (case-insensitive)
			if name != None:
				surfice = Surfice.objects.get(name__iexact=name)
			
			# If id is set, find the Surfice that has that id
			elif id != None:
				surfice = Surfice.objects.get(id=id)
			
		except Surfice.DoesNotExist:
			pass
		return surfice
	
	# -------------------------------------
	# get_surfices(surf, name)
	#
	# Gets surfices based on the arguments provided.
	# All arguments are optional. If no arguments are provided,
	# this function gets all the surfices stored in the database
	#
	# surf			Get all surfices belonging to a Surf object
	# name			Get all surfices that CONTAIN this name (case insensitive)
	# [both]		If both surf and name are set, get all Surfices that belong
	#				to the Surf object and that contain this name
	# [none]		If no params are passed, get all Surfices
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
				surfices = Surfice.objects.filter(surf=surf, name__icontains=name)
			
			# If surf is set, find all Surfice objects with that Surf
			elif surf != None:
				# CHECK TO SEE IF THIS IS REAL SURF OBJECT
				surfices = Surfice.objects.filter(surf=surf)
				
			# If name is set, find all Surfices that contain that name
			elif name != None:
				surfices = Surfice.objects.filter(name__icontains=name)
			
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
		elif Surfice.objects.filter(name__iexact='name').count() == 0:
			self.name = name
			self.save()
			code = True
		return code
	
	# -------------------------------------
	# set_surf(self, surf)
	# 
	# Sets the surf of the surfice and saves it to the database.
	# Only runs if Surf object exists in database. If it doesn't,
	# nothing happens
	# 
	# INPUT
	# surf			The surf object that this surfice will be set to
	#
	# -------------------------------------
	def set_surf(self, surf):
		# Check to make sure Surf is actually in the database
		if Surf.is_saved(surf.name):
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
		# Set the description to the new description
		self.description = description
		
		# Save this object to the database
		self.save()
	
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
			Event.create(self, status, description)
		
		self.status = status
		self.save()
	
	# -------------------------------------
	# save_new(self, *args, **kwargs)
	#
	# Saves a NEW Surfice object to the database. If a Surfice with the same name
	# already exists, nothing happens.
	#
	# RETURNS
	# True if it saved
	# False if it didn't
	# -------------------------------------
	def save_new(self, *args, **kwargs):
		# Check to see if Surfice object is already in database. Don't do anything if so
		if Surfice.is_saved(self.name):
			# Do nothing
			flag = False
		else:
			# Call the real save() method
			super(Surfice, self).save(*args, **kwargs)
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
		if Surfice.objects.filter(name__iexact=name).count() == 0:
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
# Status		create(name, description)
# void			delete(self, *args, **kwargs)
# Status		get_status(name, id)
# *Status		get_statuses(name)
# bool			set_name(self, name)
# void			set_description(self, description)
# bool			is_saved(name)
######void set_default()		Set this status as the default
# -----------------------------------------
class Status(models.Model):
	# Class variables
	name 		= models.CharField(max_length=512, unique=True)
	description = models.TextField()
	
	def __unicode__(self):
		return self.name
	
	# -------------------------------------
	# @staticmethod create(name, description)
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
	def create(name, description=''):
		status = None
		
		# Check to make sure a Status object with the same name
		# isn't already in the database.
		if Status.objects.filter(name__iexact=name).count() == 0:
			# Create the Status object
			status = Status()
			
			# Set the Status class variables
			status.name = name
			status.description = description
			
			# Save the Status object to the database
			status.save()
		
		return status
	
	# -------------------------------------
	# delete(self, *args, **kwargs)
	#
	# INPUT
	# args, kwargs			Only for extension of the built-in function
	# 
	# Deletes this status from the database
	# -------------------------------------
	def delete(self, *args, **kwargs):
		# Call the real delete() function
		super(Status, self).delete(*args, **kwargs)
	
	# -------------------------------------
	# @staticmethod get_status(name)
	# 
	# Gets a status object by name OR id. If no parameter is
	# passed, nothing is returned
	#
	# INPUT
	# name (optional)		The name of the status
	# id (optional)			The id of the status
	#
	# RETURNS
	# A status object if found
	# If nothing is found, nothing is returned
	# -------------------------------------
	@staticmethod
	def get_status(name=None, id=None):
		# Default value to return is nothing
		status = None
		
		try:
			# If name is set, get the status that has that name
			if name != None:
				status = Status.objects.get(name__iexact=name)

			# If id is set, get the status with that id
			elif id != None:
				status = Status.objects.get(id=id)
			
		# If nothing is found, do nothing
		except Status.DoesNotExist:
			pass
		
		return status
	
	
	
	# -------------------------------------
	# @staticmethod get_statuses()
	# 
	# Gets a list of all the statuses
	#
	# INPUT
	# name (optional)		Find statuses that contain this name
	#
	# RETURNS
	# An array of statuses (empty if nothing found)
	# -------------------------------------
	@staticmethod
	def get_statuses(name=None):
		
		# If no statuses are found, return an empty array
		statuses = []
		
		try: 
			# If name is set, find all statuses that contain that name (case insensitive)
			if name != None:
				statuses = Status.objects.filter(name__icontains=name)
	
			# If no params are passed, get all the statuses in the database
			else:
				statuses = Status.objects.all()
		
		# If nothing is found, do nothing
		except Status.DoesNotExist:
			pass
		
		return statuses
	
	# -------------------------------------
	# set_name(self, name)
	#
	# Sets the name of the status to a new unique name
	#
	# INPUT
	# name			The new name of the status object
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
		elif Status.objects.filter(name__iexact='name').count() == 0:
			self.name = name
			self.save()
			code = True
		return code
	
	# -------------------------------------
	# set_description(self, description)
	#
	# Sets the description of the status and saves it to the database
	#
	# INPUT
	# description			The new description of the status object
	# -------------------------------------
	def set_description(self, description):
		# Set the description to the new description
		self.description = description
		
		# Save this object to the database
		self.save()
	
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
		if Status.objects.filter(name__iexact=name).count() == 0:
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
# status			Status object that the user is reporting
# email				Email of the user who submitted an ding
# description		Description of the ding
# NEED TO ADD RESOLVED FIELD
#
# METHODS
# Ding			create(surfice, status, email, description)
# *Ding			get_dings(...)
# 
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
	# @staticmethod create(surfice, status, email, description)
	# 
	# Creates an ding for the set surfice and stores it in the database
	#
	# INPUT
	# surfice					The surfice object that has a ding
	# status					The reported status of the surfice
	# email						The email address of the person who submitted the ding
	# description (optional)	Description of the event
	#
	# RETURNS
	# The created ding
	# -------------------------------------
	@staticmethod
	def create(surfice, status, email, description=''):
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
	
	# -------------------------------------
	# @staticmethod get_ding(id)
	# 
	# Get ding that corresponds to the id parameter. If no param is passed
	# nothing is returned
	#
	# INPUT
	# id			id of the Ding
	#
	# RETURNS
	# Ding corresponding to the id
	# None if nothing is found
	# -------------------------------------
	@staticmethod
	def get_ding(id):
		# Default value to return is nothing
		ding = None
		
		try:
			# If name is set, get the ding that has that name
			ding = Ding.objects.get(id=id)
			
		# If nothing is found, do nothing
		except Ding.DoesNotExist:
			pass
		
		return Ding
	
	# -------------------------------------
	# @staticmethod get_dings(**kwargs)
	# 
	# Get Dings in reverse chronological order (newest first)
	# from the database based on the arguments.
	# All arguments are optional, and only one at time can be used
	# (other than the start, end variables)
	# If no argument is passed, all Dings are returned
	# 
	#
	# INPUT
	# surfice		Dings related to a Surfice object
	# email			The email address of the person who submitted the ding
	# status		The reported status stored in the Ding
	# days			int in number of days back from the current day to pull dings
	# events		int number of dings to pull regardless of date
	# start			timestamp (YYYY-MM-DD) of the start date of dings
	# end			timestamp (YYYY-MM-DD) of the end date. Gets dings
	#				from before and including this date
	# start, end	if both are set, all dings between (inclusive)
	#				will be returned
	# [none]		If no argument is passed, all stored Dings will be returned
	#
	# RETURNS
	# Array of Dings in reverse chronological order (newest first)
	# -------------------------------------
	@staticmethod
	def get_dings(**kwargs):
		
		# Empty array of dings
		dings = []
		
		# Get all dings related to a specific surfice
		if 'surfice' in kwargs:
			surfice = kwargs['surfice']
			dings = Ding.objects.filter(surfice=surfice).order_by('-timestamp', '-id')
		
		# Get all dings related to a specific email
		elif 'email' in kwargs:
			email = kwargs['email']
			dings = Ding.objects.filter(email=email).order_by('-timestamp', '-id')
		
		# Get all dings that report a specific status
		elif 'status' in kwargs:
			status = kwargs['status']
			dings = Ding.objects.filter(status=status).order_by('-timestamp', '-id')
		
		# Get all dings in the past x days
		elif 'days' in kwargs:
			x = kwargs['days']
			start = date.today() - timedelta(x)
			# Equivalent in SQL to SELECT ... WHERE timestamp >= start
			dings = Ding.objects.filter(timestamp__gte=start).order_by('-timestamp', '-id')
			
		# Get the past x number of events	
		elif 'dings' in kwargs:
			x = kwargs['events']
			dings = Ding.objects.all().order_by('-timestamp', '-id')[:x]
		
		# Get dings up to the current date from the start date
		# If end is set, get dings between (inclusive) these dates			
		elif 'start' in kwargs:
			start = kwargs['start']
			
			# If end is set, get dings up to and including that date
			# Else, just use the current date
			if 'end' in kwargs:
				end = kwargs['end']
				dings = Ding.objects.filter(timestamp__gte=start, timestamp__lte=end).order_by('-timestamp', '-id')
				
			else:
				end = date.today()
				dings = Ding.objects.filter(timestamp__gte=start).order_by('-timestamp', '-id')

		# Get events up to and including the end date
		elif 'end' in kwargs:
			end = kwargs['end']
			dings = Ding.objects.filter(timestamp__lte=end).order_by('-timestamp', '-id')
			
		# If no argument is given, get all events 
		else:
			dings = Ding.objects.all().order_by('-timestamp', '-id')
			
		
		return dings



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
#
# METHODS
# Event			create(surfice, status, description)
# void			delete(self, *args, **kwargs)
# *Event		get_events(...)
###### Need to make setter function######################################
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
	# @staticmethod create(surfice, status, description)
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
	def create(surfice, status, description=''):
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
	# delete(self, *args, **kwargs)
	#
	# INPUT
	# args, kwargs			Only for extension of the built-in function
	# 
	# Deletes this event from the database
	# -------------------------------------
	def delete(self, *args, **kwargs):
		# Call the real delete() function
		super(Event, self).delete(*args, **kwargs)
	
	# -------------------------------------
	# @staticmethod get_event(id)
	# 
	# Get event that corresponds to the id parameter. If no param is passed
	# nothing is returned
	#
	# INPUT
	# id			id of the Event
	#
	# RETURNS
	# Event corresponding to the id
	# None if nothing is found
	# -------------------------------------
	@staticmethod
	def get_event(id):
		# Default value to return is nothing
		event = None
		
		try:
			# If name is set, get the event that has that name
			event = Event.objects.get(id=id)
			
		# If nothing is found, do nothing
		except Event.DoesNotExist:
			pass
		
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
	# NEED TO ADD GET ALL EVENTS THAT HAPPENED WITH A SPECIFIC SURFICE OR SURF
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

			

