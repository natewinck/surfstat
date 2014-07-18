from django.db import models

from yamlfield.fields import YAMLField

from datetime import date, timedelta


# -------------------------------------
# Surf Class
#
# Group container for a set of Surfices
#
# CLASS VARIABLES
# name			Name of the Surf
# description	Description of the Surf
# data			Generic data field stored as separate keys
#
# METHODS
# String		__unicode__(self)
# Surf			create(name, description)
# void			delete(self, *args, **kwargs)
# Surf			get_surf(name, pk, id)
# *Surf			get_surfs(name)
# *Surfice 		get_surfices(self, name)
# void			set(self, name, description, **kwargs)
# bool			set_name(self, name)
# void			set_description(self, description)
# bool			save_new(self, *args, **kwargs)
# bool			is_saved(name, pk, surf)
#
# -------------------------------------
class Surf(models.Model):
	# Class variables
	name 		= models.CharField(max_length=512, unique=True)
	description = models.TextField(blank=True)
	data		= YAMLField()
	
	# Class methods
	def __unicode__(self):
		return self.name
	
	# -------------------------------------
	# @staticmethod create(name, description, **kwargs)
	#
	# Creates a Surf object in the database defined by the given name and description
	# 
	# INPUT
	# name (required)			A string that gives the name of the surf
	# description (optional)	A string that describes the surf
	# kwargs					Generic data to be stored in the database as separate keys
	#
	# RETURNS
	# The created surf
	# -------------------------------------
	@staticmethod
	def create(name, description='', **kwargs):
		surf = None
		
		# Check to make sure another Surf object with the same name isn't
		# already in the database
		if not Surf.is_saved(name=name) and name.strip() != '':
			# Create the Surf object
			surf = Surf()
			
			# Set the surf attributes
			surf.name = ' '.join(name.split())
			surf.description = description
			
			# Set any generic data that might've been passed
			for key in kwargs:
				surf.data[key] = kwargs[key]
			
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
			if Surf.objects.filter(pk=self.pk).count() != 0:
				# Call the real delete() function
				super(Surf, self).delete(*args, **kwargs)
		except Surf.DoesNotExist:
			pass
	
	# --------------------------
	# @staticmethod get_surf(name)
	#
	# Get a Surf object by name OR id/pk from the database
	#
	# INPUT
	# name			The name of the Surf object
	# id = pk		The id/primary key of the Surf object
	#
	# RETURNS
	# A Surf object
	# None if no object found
	# ---------------------------
	@staticmethod
	def get_surf(name=None, pk=None, id=None):
		surf = None
		
		if name != None:
			try:
				surf = Surf.objects.get(name__iexact=name)
			except Surf.DoesNotExist:
				pass

		elif id != None or pk != None:
			# If pk is not set (meaning id is set), use id
			if pk == None:
				pk = id
			
			try:
				surf = Surf.objects.get(pk=pk)
			except Surf.DoesNotExist:
				pass


		return surf
	
	# --------------------------
	# @staticmethod get_surfs()
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
	# An Array of surfices if they are found
	# -------------------------------------
	def get_surfices(self, name=None):
		surfices = []
		try:
			# Find all Surfice objects that are in this surf
			# and that also contain the name param
			if name != None:
				# surfices is a reverse lookup defined by the related name in the Surfice class
				surfices = Surf.objects.get(id=self.id).surfice_set.filter(name__icontains=name)
			
			# If name is not set, get all Surfices under this Surf
			else:
				surfices = Surf.objects.get(id=self.id).surfice_set.all()
		
		except Surf.DoesNotExist:
			# We get here if we didn't find the specified category.
			# Don't do anything - the template displays the "no category" message for us.
			pass
		
		return surfices
	
	# -------------------------------------
	# set(self, name, description, **kwargs)
	#
	# Generic setter function. All fields are optional, but nothing happens
	# if no parameters are passed
	#
	# INPUT
	# name (optional)			The new name of the surf object
	# description (optional)	The new description of the surf object
	# kwargs					Any other fields that would go into the generic data field as keys
	# -------------------------------------
	def set(self, name=None, description=None, **kwargs):
		
		# If name is set, name hasn't changed, name isn't blank, and there isn't another object
		# with the same name (case insensitive), update the name
		if name != None:
			self.set_name()
		
		# If description is set, change the description
		if description != None:
			self.set_description(description)
		
		# Go through the generic data and put it in their respective fields
		for key in kwargs:
			self.data[key] = kwargs[key]
		
		# Save the object to the database
		self.save()
	
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
		if ' '.join(name.split()) == self.name:
			code = False
		
		# Check if new name already exists in database
		# If new name doesn't exist, set this object to that name	
		elif not Surf.is_saved(name=name, exclude=self.id) and name.strip() != '':
			self.name = ' '.join(name.split())
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
		if Surf.is_saved(name=self.name):
			# Do nothing
			flag = False
		elif name.strip() != '':
			# Call the real save() method
			self.name = ' '.join(self.name.split())
			super(Surf, self).save(*args, **kwargs)
			flag = True
		
		return flag
	
	# -------------------------------------
	# @staticmethod is_saved(name, pk, surf)
	# 
	# Checks to see if Surf object is already in database.
	# 
	# INPUT
	# name (optional)	Name of the Surf object
	# pk (optional)		Private key of the Surf object
	# surf (optional)	Surf object
	# exclude (optional)	pk of surf object to exclude from name search
	# 
	# RETURNS
	# True if Surf object is in database
	# False if Surf object is not in database
	# -------------------------------------
	@staticmethod
	def is_saved(name=None, pk=None, surf=None, exclude=-1):
		exists = False
		
		if name != None and Surf.objects.filter(name__iexact=' '.join(name.split())).exclude(pk=exclude).count() > 0:
			exists = True
		
		elif pk != None and Surf.objects.filter(pk=pk).count() > 0:
			exists = True
		
		elif type(surf) is Surf and Surf.objects.filter(pk=surf.pk).exists():
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
# data			Generic data stored as keys
#
# METHODS
# String			__unicode__(self)
# Surfice			create(name, surfs, description, **kwargs)
# void				delete(self, *args, **kwargs)
# Surfice			get_surfice(name, pk, id)
# *Surfice			get_surfices(...)
# Status			get_status(self)
# *Event			get_events(self, ...)
# void				set(self, name, surfs, description, **kwargs)
# bool				set_name(self, name)
# void				set_surf(self, surf)
# void				set_surfs(self, surfs)
# void				add_surf(self, surf)
# void				add_surfs(self, surfs)
# void				set_description(self, description)
# void				set_status(self, status, description)
# bool				save_new(self, *args, **kwargs)
# bool				is_saved(name, pk, surfice)
# 
# -------------------------------------
class Surfice(models.Model):
	# Class variables
	name 		= models.CharField(max_length=512, unique=True)
	
	# Reason for not using related_name:
	# In this case, the related_name would be 'surfices' so 
	# that you can do things like surf.surfices and it looks clean.
	# Unfortunately when it came to templating, I need the 'surfices'
	# namespace to make it clear there. I figured if there was a place
	# to be more clear, it would be on the design side.
	# Thus, instead of using 'surfices' we use the default 'surfice_set'
	surfs 		= models.ManyToManyField(Surf, blank=True)
	
	description = models.TextField(blank=True)
	status		= models.ForeignKey('Status')
	data		= YAMLField()
	
	def __unicode__(self):
		return self.name
	
	#def __init__(self):
	#	self.name = "Default"
	#	self.description = "Default description"
	#	self.group = Surf()
	
	# -------------------------------------
	# @staticmethod create(name, surfs, description, **kwargs)
	# 
	# Create a new Surfice object and store it in the database
	# 
	# INPUT
	# name						Name of the Surfice
	# surfs						Surf object array that this Surfice belongs to
	# status					Status object that Surfice has
	# description (optional)	Description of the Surfice
	# kwargs (optional)			Generic data stored as keys
	# 
	# RETURNS
	# The created Surfice object
	# -------------------------------------
	@staticmethod
	def create(name, surfs, status, description='', **kwargs):
		surfice = None
		
		# Check to make sure a Surfice object with the same name
		# isn't already in the database.
		if not Surfice.is_saved(name=name) and name.strip() != '':
			print "inside"
			# Create the Surfice object
			surfice = Surfice()
			
			# Set the Surfice class variables
			# Remove extra spaces from the name
			surfice.name = ' '.join(name.split())
			surfice.description = description
			surfice.status = status
			
			# Add generic data
			for key in kwargs:
				surfice.data[key] = kwargs[key]
			
			# Save the Surfice object to the database
			surfice.save()
			
			# Now that the Surfice object has been saved,
			# associate it with surf objects 
			surfice.surfs = surfs
		
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
	# get_surfice(name, pk, id)
	# 
	# Gets the surfice with the defined name OR id/pk
	# 
	# INPUT
	# name			The name of the surfice
	# id = pk		id/primary key of the surfice
	#
	# RETURNS
	# A surfice object
	# None if no surfice found
	# -------------------------------------
	@staticmethod
	def get_surfice(name=None, pk=None, id=None):
		surfice = None
		try:
			# If name is set, find the Surfice whose name matches (case-insensitive)
			if name != None:
				surfice = Surfice.objects.get(name__iexact=name)
			
			# If id is set, find the Surfice that has that id
			elif pk != None or id != None:
				# If pk is not set (meaning id is set), use id
				if pk == None:
					pk = id
				
				surfice = Surfice.objects.get(pk=pk)
			
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
	def get_surfices(surf=None, name=None, status=None):
		
		try:
			
			# If both surf and name are set, find all objects with that Surf
			# and contain the name
			if surf != None and name != None:
				surfices = Surfice.objects.filter(surfs=surf, name__icontains=name)
			
			# If surf is set, find all Surfice objects with that Surf
			elif surf != None:
				# CHECK TO SEE IF THIS IS REAL SURF OBJECT
				surfices = Surfice.objects.filter(surfs=surf)
				
			# If name is set, find all Surfices that contain that name
			elif name != None:
				surfices = Surfice.objects.filter(name__icontains=name)
			
			# If status is set, find all Surfices that have this status
			elif status != None:
				surfices = Surfice.objects.filter(status=status)
			
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
		# Get events
		events = Event.get_events(surfice=self)
		return events
	
	# -------------------------------------
	# set(self, name, surfs, description, **kwargs)
	#
	# Generic setter function. All fields are optional, but nothing happens
	# if no parameters are passed
	#
	# INPUT
	# name (optional)			The new name of the surfice object
	# surfs (optional)			The new surf objects this surfice is part of
	# description (optional)	The new description of the surfice object
	# kwargs					Any other fields that would go into the generic data field as keys
	# -------------------------------------
	def set(self, name=None, surfs=None, description=None, **kwargs):
		
		# If name is set, name hasn't changed, name isn't blank, and there isn't another object
		# with the same name (case insensitive), update the name
		if name != None:
			self.set_name(name)
		
		# If surfs are set, update it
		if surfs != None:
			self.set_surfs(surfs)
		
		# If description is set, change the description
		if description != None:
			self.set_description(description)
		
		# Go through the generic data and put it in their respective fields
		for key in kwargs:
			self.data[key] = kwargs[key]
		
		# Save the object to the database
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
		if ' '.join(name.split()) == self.name:
			code = False
		
		# Check if new name already exists in database
		# If new name doesn't exist and isn't blank, set this object to that name	
		elif not Surfice.is_saved(name=name, exclude=self.id)  and name.strip() != '':
			self.name = ' '.join(name.split())
			self.save()
			code = True
		return code
	
	# -------------------------------------
	# set_surf(self, surf)
	# 
	# Replaces the surf(s) of the surfice with this surf and saves it to the database.
	# Only runs if Surf object exists in database. If it doesn't,
	# nothing happens
	# 
	# INPUT
	# surf			The surf object that this surfice will be set to
	#
	# -------------------------------------
	def set_surf(self, surf):
		# Check to make sure Surf is actually in the database
		if Surf.is_saved(surf=surf):
			self.surfs = [surf]
		
			# Save surfice object to database
			self.save()
	
	# -------------------------------------
	# set_surfs(self, surfs)
	# 
	# Replaces the surf(s) of the surfice with these surfs and saves it to the database.
	# 
	# INPUT
	# surfs			The surf array that this surfice will be set to
	#
	# -------------------------------------
	def set_surfs(self, surfs):
		self.surfs = surfs
	
		# Save surfice object to database
		self.save()
	
	# -------------------------------------
	# add_surf(self, surf)
	# 
	# Add a surf to this surfice and save it to the database.
	# Only runs if Surf object exists in database. If it doesn't,
	# nothing happens
	# 
	# INPUT
	# surf			The surf object that this surfice will be added to
	#
	# -------------------------------------
	def add_surf(self, surf):
		# Check to make sure Surf is actually in the database
		if Surf.is_saved(surf=surf):
			self.surfs.add(surf)
		
			# Save surfice object to database
			self.save()
	
	# -------------------------------------
	# add_surfs(self, surfs)
	# 
	# Add surfs to this surfice and save it to the database.
	# Does not check if surfs are already in database (dangerous)
	# 
	# INPUT
	# surfs			The surf objects that this surfice will be added to
	#
	# -------------------------------------
	def add_surfs(self, surfs):
		# Does NOT check if surfs are already in database (dangerous)
		# Expand the array out for .add()
		self.surfs.add(*surfs)
	
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
	# status					a Status object
	# description (optional)	If set (even to a blank string), create an
	#							event along with the status
	# -------------------------------------
	def set_status(self, status, description='', event=True):
		
		# If we want to create an event along with updating the status,
		# do it here.
		if event:
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
		if Surfice.is_saved(name=self.name):
			# Do nothing
			flag = False
		else:
			# Call the real save() method
			self.name = ' '.join(self.name.split())
			super(Surfice, self).save(*args, **kwargs)
			flag = True
		
		return flag
	
	# -------------------------------------
	# @staticmethod is_saved(name, pk, surfice)
	# 
	# Checks to see if Surfice object is already in database.
	# 
	# INPUT
	# name			Name of the Surfice object
	# pk			Private key of the surfice object
	# surfice		Surfice object
	# exclude (optional)	pk of Surfice object that you want to exclude from name search
	# 
	# RETURNS
	# True if Surfice object is in database
	# False if Surfice object is not in database
	# -------------------------------------
	@staticmethod
	def is_saved(name=None, pk=None, surfice=None, exclude=-1):
		exists = False
		print Surfice.objects.filter(name__iexact=' '.join( name.split() )).count() > 0
		# If name is set and the object is in the database
		if name != None and Surfice.objects.filter(name__iexact=' '.join( name.split() )).exclude(pk=exclude).count() > 0:
			exists = True
		
		# If pk is set and the object is in the database
		elif pk != None and Surfice.objects.filter(pk=pk).count() > 0:
			exists = True
		
		# If surfice is set, check to see if it's in the database
		elif type(surfice) is Surfice and Surfice.objects.filter(surfice=surfice).count() > 0:
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
# data			Generic data
#
# METHODS
# 
# Status		create(name, description)
# void			delete(self, *args, **kwargs)
# Status		get_status(name, pk, id)
# *Status		get_statuses(name)
# void			set(self, name, description, **kwargs)
# bool			set_name(self, name)
# void			set_description(self, description)
# bool			is_saved(name, pk, status)
# -----------------------------------------
class Status(models.Model):
	# Class variables
	name 		= models.CharField(max_length=512, unique=True)
	description = models.TextField(blank=True)
	data		= YAMLField()
	
	def __unicode__(self):
		return self.name
	
	# -------------------------------------
	# @staticmethod create(name, description, **kwargs)
	#
	# Create a new status with name and optional description
	#
	# INPUT
	# name						Name of the status
	# description (optional)	Description of the status
	# kwargs (optional)			Generic data to be put in the database
	#
	# RETURNS
	# The created Status object
	# -------------------------------------
	@staticmethod
	def create(name, description='', **kwargs):
		status = None
		
		# Check to make sure a Status object with the same name
		# isn't already in the database.
		if not Status.is_saved(name=name) and name.strip() != '':
			# Create the Status object
			status = Status()
			
			# Set the Status class variables
			# Remove extra spaces from the name
			status.name = ' '.join(name.split())
			status.description = description
			
			# Set a default color
			status.data = {'color': '#ffffff'}
			
			# Loop through the kwargs and add them to the generic data field jdata
			for key in kwargs:
				status.data[key] = kwargs[key]
			
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
	# Gets a status object by name OR id/pk. If no parameter is
	# passed, nothing is returned
	#
	# INPUT
	# name (optional)		The name of the status
	# id=pk (optional)		The id/primary key of the status
	#
	# RETURNS
	# A status object if found
	# If nothing is found, nothing is returned
	# -------------------------------------
	@staticmethod
	def get_status(name=None, pk=None, id=None):
		# Default value to return is nothing
		status = None
		
		try:
			# If name is set, get the status that has that name
			if name != None:
				status = Status.objects.get(name__iexact=name)

			# If id or pk is set, get the status with that pk or id
			elif pk != None or id != None:
				# If pk is not set (meaning id is set), use id
				if pk == None:
					pk = id
				status = Status.objects.get(pk=pk)
			
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
	# set(self, name, description, **kwargs)
	#
	# Generic setter function. All fields are optional, but nothing happens
	# if no parameters are passed
	#
	# INPUT
	# name (optional)			The new name of the status object
	# description (optional)	The new description of the status object
	# kwargs					Any other fields that would go into the generic data field
	# -------------------------------------
	def set(self, name=None, description=None, **kwargs):
		
		# If name is set, name hasn't changed, and there isn't another object
		# with the same name, update the name
		if name != None:
			self.set_name(name)
		
		# If description is set, change the description
		if description != None:
			self.set_description(description)
		
		# Go through the generic data and put it in their respective fields
		for key in kwargs:
			self.data[key] = kwargs[key]
		
		# Save the object to the database
		self.save()
	
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
		if ' '.join(name.split()) == self.name:
			code = False
		
		# Check if new name already exists in database
		# If new name doesn't exist and isn't blank, set this object to that name	
		elif not Status.is_saved(name=name, exclude=self.id) and name.strip() != '':
			self.name = ' '.join(name.split())
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
	# @staticmethod is_saved(name, pk, status)
	# 
	# Checks to see if Status object is already in database.
	# 
	# INPUT
	# name			Name of the Status object
	# pk			Private key of the object
	# status		Status object
	# exclude (optional)	pk of status object to exclude from name search
	# 
	# RETURNS
	# True if Status object is in database
	# False if Status object is not in database
	# -------------------------------------
	@staticmethod
	def is_saved(name=None, pk=None, status=None, exclude=-1):
		exists = False
		
		# If name is set and the object is in the database
		if name != None and Status.objects.filter(name__iexact=' '.join(name.split())).exclude(pk=exclude).count() > 0:
			exists = True
		
		# If pk is set and the object is in the database
		elif pk != None and Status.objects.filter(pk=pk).count() > 0:
			exists = True
		
		# If surfice is set, check to see if it's in the database
		elif type(status) is Status and Status.objects.filter(status=status).count() > 0:
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
# data				Generic data stored as keys
# NEED TO ADD RESOLVED FIELD
#
# METHODS
# Ding			create(surfice, status, email, description)
# Ding			get_ding(pk)
# *Ding			get_dings(...)
# 
# -----------------------------------------
class Ding(models.Model):
	# Class variables
	timestamp	= models.DateTimeField(auto_now=False, auto_now_add=True)
	surfice		= models.ForeignKey(Surfice)
	status		= models.ForeignKey(Status)
	email		= models.EmailField()
	description	= models.TextField(blank=True)
	data		= YAMLField()
	
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
	# kwargs (optional)			Generic data stored as keys
	#
	# RETURNS
	# The created ding
	# -------------------------------------
	@staticmethod
	def create(surfice, status, email, description='', **kwargs):
		# Create the Ding object
		ding = Ding()
		ding.surfice = surfice
		ding.status = status
		ding.email = email
		ding.description = description
		
		# Go through kwargs and assign to generic data field
		for key in kwargs:
			ding.data[key] = kwargs[key]
		
		# Save the Ding object to the database
		ding.save()
		
		return ding
	
	# -------------------------------------
	# @staticmethod get_ding(pk)
	# 
	# Get ding that corresponds to the pk parameter. If no param is passed
	# nothing is returned
	#
	# INPUT
	# pk			primary key of the Ding
	#
	# RETURNS
	# Ding corresponding to the primary key
	# None if nothing is found
	# -------------------------------------
	@staticmethod
	def get_ding(pk):
		# Default value to return is nothing
		ding = None
		
		# If pk is less than 0, it is an error
		#if int(pk) >= 0:
		try:
			# If name is set, get the ding that has that name
			ding = Ding.objects.get(pk=pk)
		
		# If nothing is found, do nothing
		except Ding.DoesNotExist:
			pass
		
		return ding
	
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
	# [sort, sort_by,
	# order, order_by] 	Allows custom sorting, and then sorting by
	#					timestamp and then pk
	# [none]		If no argument is passed, all stored Dings will be returned
	#
	# RETURNS
	# Array of Dings in reverse chronological order (newest first)
	# -------------------------------------
	@staticmethod
	def get_dings(**kwargs):
		
		# Empty array of dings
		dings = []
		
		# Get how to sort the events and add it to the order_by array
		order_by = ['-timestamp', '-pk']
		if 	 'sort' 	in kwargs: order_by.insert(0, kwargs['sort'])
		elif 'sort_by' 	in kwargs: order_by.insert(0, kwargs['sort_by'])
		elif 'order' 	in kwargs: order_by.insert(0, kwargs['order'])
		elif 'order_by' in kwargs: order_by.insert(0, kwargs['order_by'])
		
		# Ignoring the '-' to reverse the order, check to make sure that the field
		# we are trying to sort by actually exists
		# If it doesn't exist, just do the default -timestamp, -pk ordering
		if not order_by[0].replace('-', '') in ['timestamp', 'surfice', 'status', 'email', 'description', 'id', 'pk']:
			order_by.pop(0)
		
		# For the foreign keys, order by name rather than their arbitrary pks
		# e.g. 'status' becomes 'status__name'
		elif order_by[0].replace('-', '') in ['status', 'surfice']:
			order_by[0] += '__name'
		
		# Get all dings related to a specific surfice
		if 'surfice' in kwargs:
			surfice = kwargs['surfice']
			dings = Ding.objects.filter(surfice=surfice).order_by(*order_by)
		
		# Get all dings related to a specific email
		elif 'email' in kwargs:
			email = kwargs['email']
			dings = Ding.objects.filter(email=email).order_by(*order_by)
		
		# Get all dings that report a specific status
		elif 'status' in kwargs:
			status = kwargs['status']
			dings = Ding.objects.filter(status=status).order_by(*order_by)
		
		# Get all dings in the past x days
		elif 'days' in kwargs:
			x = kwargs['days']
			start = date.today() - timedelta(x)
			# Equivalent in SQL to SELECT ... WHERE timestamp >= start
			dings = Ding.objects.filter(timestamp__gte=start).order_by(*order_by)
			
		# Get the past x number of events	
		elif 'dings' in kwargs:
			x = kwargs['events']
			dings = Ding.objects.all().order_by(*order_by)[:x]
		
		# Get dings up to the current date from the start date
		# If end is set, get dings between (inclusive) these dates			
		elif 'start' in kwargs:
			start = kwargs['start']
			
			# If end is set, get dings up to and including that date
			# Else, just use the current date
			if 'end' in kwargs:
				end = kwargs['end']
				dings = Ding.objects.filter(timestamp__gte=start, timestamp__lte=end).order_by(*order_by)
				
			else:
				end = date.today()
				dings = Ding.objects.filter(timestamp__gte=start).order_by(*order_by)

		# Get events up to and including the end date
		elif 'end' in kwargs:
			end = kwargs['end']
			dings = Ding.objects.filter(timestamp__lte=end).order_by(*order_by)
			
		# If no argument is given, get all events 
		else:
			dings = Ding.objects.all().order_by(*order_by)
			
		
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
# surfice			Surfice object that event affects
# description		description of the event
# data				Generic data stored as keys
#
# METHODS
# Event			create(surfice, status, description)
# void			delete(self, *args, **kwargs)
# *Event		get_events(...)
# void			set(status, surfice, description, **kwargs)
# ---------------------------------------
class Event(models.Model):
	# Class variables
	timestamp	= models.DateTimeField(auto_now_add=True, auto_now=False)
	status		= models.ForeignKey(Status)
	surfice		= models.ForeignKey(Surfice)
	description	= models.TextField(blank=True)
	data		= YAMLField()
	
	def __unicode__(self):
		return self.status.name
	
	# -------------------------------------
	# @staticmethod create(surfice, status, description, **kwargs)
	# 
	# Creates an event for the set surfice. The surfice's status is also updated
	#
	# INPUT
	# surfice					The surfice object that has an event
	# status					The new status of the surfice
	# description (optional)	Description of the event
	# kwargs (optional)			Generic data stored as keys
	#
	# RETURNS
	# The created event
	# -------------------------------------
	@staticmethod
	def create(surfice, status, description='', **kwargs):
		# Probably need to check these before setting them
		event = Event()
		
		# Set the event attributes
		event.surfice = surfice
		event.status = status
		event.description = description
		
		# Loop through kwargs and store as generic data in the database
		for key in kwargs:
			event.data[key] = kwargs[key]
		
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
	# @staticmethod get_event(pk)
	# 
	# Get event that corresponds to the pk parameter. If no param is passed
	# nothing is returned
	#
	# INPUT
	# pk			primary key of the Event
	#
	# RETURNS
	# Event corresponding to the primary key
	# None if nothing is found
	# -------------------------------------
	@staticmethod
	def get_event(pk):
		# Default value to return is nothing
		event = None
		
		try:
			# If name is set, get the event that has that name
			event = Event.objects.get(pk=pk)
			
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
	# days				int in number of days back from the current day to pull events
	# events			int number of events to pull regardless of date
	# start				timestamp (YYYY-MM-DD) of the start date of events
	# end				timestamp (YYYY-MM-DD) of the end date. Gets events
	#					from before and including this date
	# start, end		if both are set, all events between (inclusive)
	#					will be returned
	# surfice			Surfice object that has events
	# status			Status of events
	# [sort, sort_by,
	# order, order_by] 	Allows custom sorting, and then sorting by
	#					timestamp and then pk
	# [none]			If no argument is passed, all stored events will be returned
	#
	# RETURNS
	# Array of events in reverse chronological order (newest first)
	# -------------------------------------
	@staticmethod
	def get_events(**kwargs):
		
		# Empty array of events
		events = []
		
		# Get how to sort the events and add it to the order_by array
		order_by = ['-timestamp', '-pk']
		if 	 'sort' 	in kwargs: order_by.insert(0, kwargs['sort'])
		elif 'sort_by' 	in kwargs: order_by.insert(0, kwargs['sort_by'])
		elif 'order' 	in kwargs: order_by.insert(0, kwargs['order'])
		elif 'order_by' in kwargs: order_by.insert(0, kwargs['order_by'])
		
		# Ignoring the '-' to reverse the order, check to make sure that the field
		# we are trying to sort by actually exists
		# If it doesn't exist, just do the default -timestamp, -pk ordering
		if not order_by[0].replace('-', '') in ['description', 'id', 'pk', 'status', 'surfice', 'timestamp']:
			order_by.pop(0)
		
		# For the foreign keys, order by name rather than their arbitrary pks
		# e.g. 'status' becomes 'status__name'
		elif order_by[0].replace('-', '') in ['status', 'surfice']:
			order_by[0] += '__name'
		
		# Get all events in the past x days
		if   'days' in kwargs:
			x = kwargs['days']
			start = date.today() - timedelta(x)
			# Equivalent in SQL to SELECT ... WHERE timestamp >= start
			events = Event.objects.filter(timestamp__gte=start).order_by(*order_by)
			
		# Get the past x number of events	
		elif 'events' in kwargs:
			x = kwargs['events']
			events = Event.objects.all().order_by(*order_by)[:x]
		
		# Get events up to the current date from the start date
		# If end is set, get events between (inclusive) these dates			
		elif 'start' in kwargs:
			start = kwargs['start']
			
			# If end is set, get events up to and including that date
			# Else, just use the current date
			if 'end' in kwargs:
				end = kwargs['end']
				events = Event.objects.filter(timestamp__gte=start, timestamp__lte=end).order_by(*order_by)
				
			else:
				end = date.today()
				events = Event.objects.filter(timestamp__gte=start).order_by(*order_by)

		# Get events up to and including the end date
		elif 'end' in kwargs:
			end = kwargs['end']
			events = Event.objects.filter(timestamp__lte=end).order_by(*order_by)
		
		# Get all events associated with this surfice
		elif 'surfice' in kwargs:
			events = Event.objects.filter(surfice=kwargs['surfice']).order_by(*order_by)
		
		# Get all events that have a certain status
		elif 'status' in kwargs:
			events = Event.objects.filter(status=kwargs['status']).order_by(*order_by)
		
		# If no argument is given, get all events 
		else:
			events = Event.objects.all().order_by(*order_by)
			
		
		return events
	
	# -------------------------------------
	# set(self, status, description, **kwargs)
	#
	# Generic setter function. All fields are optional, but nothing happens
	# if no parameters are passed
	#
	# INPUT
	# status (optional)			The new name of the event
	# surfice (optional)		The new surfice of the event
	# description (optional)	The new description of the event
	# kwargs					Any other fields that would go into the generic data field as keys
	# -------------------------------------
	def set(self, status=None, surfice=None, description=None, timestamp=None, **kwargs):
		
		# If status is set and is in the database, update it
		if	(
				status != None and
				type(status) is Status and
				Status.objects.filter(pk=status.pk).count() == 1
			):
			self.status = status
		
		# If surfice is set and is in the database, update it
		if	(
				surfice != None and
				type(surfice) is Surfice and
				Surfice.objects.filter(pk=surfice.pk).count() == 1
			):
			self.surfice = surfice
		
		# If description is set, change the description
		if description != None:
			self.description = description
		
		# If timestamp is set, change the timestamp
		if timestamp != None:
			self.timestamp = timestamp
		
		# Go through the generic data and put it in their respective fields
		for key in kwargs:
			self.data[key] = kwargs[key]
		
		# Save the object to the database
		self.save()
		
		return True

