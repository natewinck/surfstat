from django.db import models

from yamlfield.fields import YAMLField

from datetime import date, timedelta


class Surf(models.Model):
	""" Group container for a set of Surfices
		
		CLASS VARIABLES
		name			Name of the Surf
		description		Description of the Surf
		data			Generic data field stored as separate keys
		
		METHODS
		String			__unicode__(self)
		Surf			create(name, description, **kwargs)
		void			delete(self, *args, **kwargs)
		Surf			get_surf(name, pk, id)
		*Surf			get_surfs(name)
		*Surfice		get_surfices(self, name)
		void			set(self, name, description, **kwargs)
		bool			set_name(self, name)
		void			set_description(self, description)
		bool			save_new(self, *args, **kwargs)
		bool			is_saved(name, pk, surf)
	"""
	
	# Class variables
	name 		= models.CharField(max_length=512, unique=True)
	description = models.TextField(blank=True)
	data		= YAMLField()
	
	# Class methods
	def __unicode__(self):
		return self.name
	
	@staticmethod
	def create(name, description='', **kwargs):
		""" Create a Surf object in the database
			
			Uses the given name and description to set the attributes
			
			INPUT
			name (required)			A string that gives the name of the surf
			description (optional)	A string that describes the surf
			kwargs					Generic data to be stored in the database as separate keys
			
			RETURNS
			the created surf
		"""
		
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
	
	def delete(self, *args, **kwargs):
		""" Delete this surf from the database
			
			INPUT
			*args, **kwargs		For extension of the built-in delete() function
		"""
		
		# Check to make sure the Surf object is in the database first
		try:
			if Surf.objects.filter(pk=self.pk).count() != 0:
				# Call the real delete() function
				super(Surf, self).delete(*args, **kwargs)
		except Surf.DoesNotExist:
			pass
	
	@staticmethod
	def get_surf(name=None, pk=None, id=None):
		""" Get a surf object by name or id from the database
			
			INPUT
			name		Name of the surf object
			id/pk		The primary key of the surf object
			
			RETURNS
			Surf object
			None if no object found
		"""
		
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
	
	@staticmethod
	def get_surfs(name=None):
		""" Get surfs from the database
			
			If name is set, find all surfs that contain the name (case insensitive).
			If nothing is set, get all surfs from the database.
			
			INPUT
			name (optional)		The name of the surf to search for
			
			RETURNS
			*Surf
			Empty array if none found
		"""
		
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
	
	def get_surfices(self, name=None):
		""" Get surfices from the database
			
			If name is set, filter surfices to ones that contain that name (case
			insensitive).  If nothing is set, get all surfices from the database.
			
			INPUT
			name (optional)		The name of the surfice to filter by
			
			RETURNS
			*Surfice
			Empty array if none found
		"""
		
		surfices = []
		try:
			# Find all Surfice objects that are in this surf
			# and that also contain the name param
			if name != None:
				# surfices is a reverse lookup defined by the related name in the Surfice class
				surfices = Surf.objects.get(id=self.id).surfices.filter(name__icontains=name)
			
			# If name is not set, get all Surfices under this Surf
			else:
				surfices = Surf.objects.get(id=self.id).surfices.all()
		
		except Surf.DoesNotExist:
			# We get here if we didn't find the specified category.
			# Don't do anything - the template displays the "no category" message for us.
			pass
		
		return surfices
	
	def set(self, name=None, description=None, **kwargs):
		""" Set components of this surf object
			
			Generic setter function. All fields are optional, but
			nothing happens if no parameters are passed.
			
			INPUT
			name (optional)			The new name of the surf object
			description (optional)	The new description of the surf object
			**kwargs				Any fields that will go into the generic data field as keys
		"""
		
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
	
	def set_name(self, name):
		""" Set name of the surf
			
			Set the name of the surf to a new unique name and save
			it to the database
			
			INPUT
			name			The new name of the surf object
			
			RETURNS
			True if set was successful
			False if failed
		"""
		
		code = False
		
		# If you aren't changing the name, don't change it!
		if ' '.join(name.split()) == self.name:
			code = True
		
		# Check if new name already exists in database
		# If new name doesn't exist, set this object to that name	
		elif not Surf.is_saved(name=name, exclude=self.id) and name.strip() != '':
			self.name = ' '.join(name.split())
			self.save()
			code = True
		return code
	
	def set_description(self, description):
		""" Set description of the surf
			
			Set the description of the surf and save it to the database
			
			INPUT
			description 		The new description of the surf object
		"""
		
		# Set this description to the new one
		self.description = description
		
		# Save this surf to the database
		self.save()
	
	def save_new(self, *args, **kwargs):
		""" Save a new surf to the database
			
			This method exists so that you can create a
			surf object manually without using the create() method.
			This saves a new object to the database. If it already exists
			in the database, don't do anything and return False.
			
			INPUT
			*args, **kwargs		Only for future extension of the save() function
			
			RETURNS
			True if saved
			Falsed if failed
		"""
		
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
	
	@staticmethod
	def is_saved(name=None, pk=None, surf=None, exclude=-1):
		""" Check if surf is saved in database
			
			This method checks by name, pk, or surf.  If checking
			by name, you have a second option: to exclude a pk. This
			is useful when checking to see if a name exists in the
			database but you don't want to check the name of your current
			surf (i.e. in form validation, you don't want to check if a surf's
			own name exists in the database...we already know it does)
			
			INPUT
			name (optional)		Name of the Surf object
			pk (optional)		Private key of the Surf object
			surf (optional)		Surf object
			exclude (optional)	pk of surf object to exclude from name search
			
			RETURNS
			True if Surf object is in database
			False if Surf object is not in database
		"""
		
		exists = False
		
		if name != None and Surf.objects.filter(name__iexact=' '.join(name.split())).exclude(pk=exclude).count() > 0:
			exists = True
		
		elif pk != None and Surf.objects.filter(pk=pk).count() > 0:
			exists = True
		
		elif type(surf) is Surf and Surf.objects.filter(pk=surf.pk).exists():
			exists = True
		
		return exists



class Surfice(models.Model):
	""" The main class.
		
		Contains information connected to various surfices that you run.
		Each has the following class variables and methods.
		
		CLASS VARIABLES
		name		Name of the surfice. Needs to be unique (case insensitive)
		surfs		Which surfs this surfice belongs to.
		description	Description of the surfice
		status		Status of Surfice
		data		Generic data stored as keys
		
		METHODS
		String		__unicode__(self)
		Surfice		create(name, surfs, description, **kwargs)
		void		delete(self, *args, **kwargs)
		Surfice		get_surfice(name, pk, id)
		*Surfice	get_surfices(surf, name, status)
		Status		get_status(self)
		*Event		get_events(self, ...)
		void		set(self, name, surfs, description, **kwargs)
		bool		set_name(self, name)
		void		set_surf(self, surf)
		void		set_surfs(self, surfs)
		void		add_surf(self, surf)
		void		add_surfs(self, surfs)
		void		set_description(self, description)
		void		set_status(self, *args, **kwargs)
		bool		save_new(self, *args, **kwargs)
		bool		is_saved(name, pk, surfice)
	"""
	
	# Class variables
	name 		= models.CharField(max_length=512, unique=True)
	
	# Reason for not using related_name:
	# In this case, the related_name would be 'surfices' so 
	# that you can do things like surf.surfices and it looks clean.
	# Unfortunately when it came to templating, I need the 'surfices'
	# namespace to make it clear there. I figured if there was a place
	# to be more clear, it would be on the design side.
	# Thus, instead of using 'surfices' we use the default 'surfice_set'
	surfs 		= models.ManyToManyField(Surf, blank=True, related_name='surfices')
	
	description = models.TextField(blank=True)
	status		= models.ForeignKey('Status')
	data		= YAMLField()
	
	def __unicode__(self):
		return self.name
	
	@staticmethod
	def create(name, surfs, status, description='', **kwargs):
		""" Create a new surfice object and store it in the database
			
			INPUT
			name					Name of the surfice
			surfs					Surf object array that this surfice belongs to
			status					Status object that the surfice has
			description (optional)	Description of the surfice
			**kwargs (optional)		Generic data stored as keys
			
			RETURNS
			the new Surfice object
		"""
		
		surfice = None
		
		# Check to make sure a Surfice object with the same name
		# isn't already in the database.
		if not Surfice.is_saved(name=name) and name.strip() != '':
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
	
	def delete(self, *args, **kwargs):
		""" Delete this surfice from the database
			
			INPUT
			*args, **kwargs		For extension of the built-in delete() function
		"""
		
		# Call the real delete() function
		super(Surfice, self).delete(*args, **kwargs)
	
	@staticmethod
	def get_surfice(name=None, pk=None, id=None):
		""" Get a surfice by name or id
			
			INPUT
			name		Name of the surfice
			id/pk		id/pk of the surfice
			
			RETURNS
			Surfice object
			None if no surfice found
		"""
		
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
	
	@staticmethod
	def get_surfices(surf=None, name=None, status=None):
		""" Gets surfices based on arguments provided
			
			If surf and name are set, get all surfices in that surf
			that contain this name.
			Otherwise if one is set, search by that parameter.
			
			surf		Get all surfices belonging to a surf object
			name		Get all surfices that contain this name (case insensitive)
			[surf,name]	Get all surfices that belong to the Surf object and that
						contain this name
			[none]		Get all surfices
			
			RETURNS
			*Surfice
		"""
		
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
	
	def get_status(self):
		""" Get status of the surfice
			
			RETURNS
			Status
		"""
		
		return self.status

	def get_events(self, **kwargs):
		""" Get events for this surfice
			
			Shortcut method to the Event.get_events() method
			
			INPUT
			(same as get_events())
			
			RETURNS
			*Event
		"""
		
		# Get events
		events = Event.get_events(surfice=self)
		return events
	
	def set(self, name=None, surfs=None, description=None, **kwargs):
		""" Set surfice components
			
			Generic setter function. All fields are optional, but
			nothing happens if no parameters are passed.
			
			INPUT
			name (optional)			The new name of the surfice object
			surfs (optional)		The new surf objects this surfice is part of
			description (optional)	The new description of the surfice object
			**kwargs				Any other generic data stored as keys
		"""
		
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
	
	def set_name(self, name):
		""" Set name of surfice
			
			Only set name if
			a) it's different
			b) it's not the same as another surfice (i.e. needs to be unique)
			
			INPUT
			name		The new name of the surfice object
			
			RETURNS
			True if set worked
			False if failed
		"""
		
		code = False
		
		# If you aren't changing the name, don't change it!
		if ' '.join(name.split()) == self.name:
			code = True
		
		# Check if new name already exists in database
		# If new name doesn't exist and isn't blank, set this object to that name	
		elif not Surfice.is_saved(name=name, exclude=self.id)  and name.strip() != '':
			self.name = ' '.join(name.split())
			self.save()
			code = True
		return code
	
	def set_surf(self, surf):
		""" Assign the surfice to a single surf
			
			Replaces any surfs that are already assigned on this surfice.
			Only runs if Surf object exists in database. If it
			doesn't, nothing happens.
			
			INPUT
			surf		Surf object that this surf will be set to
		"""
		
		# Check to make sure Surf is actually in the database
		if Surf.is_saved(surf=surf):
			self.surfs = [surf]
		
			# Save surfice object to database
			self.save()
	
	def set_surfs(self, surfs):
		""" Assign the surfice to multiple surfs
			
			Replace any surfs that are already assigned on this surfice. 
			Assumes that the surfs already exist in the database.
			
			INPUT
			surfs		Array of surfs this surfice will be assigned to
		"""
		
		self.surfs = surfs
	
		# Save surfice object to database
		self.save()
	
	def add_surf(self, surf):
		""" Assign the surfice to an additional surf
			
			Adds on to any existing surfs this surfice might already
			be assigned to.
			If the Surf object does not exist in the database,
			nothing happens.
			
			INPUT
			surf		The surf object that this surfice will be added to
		"""
		
		# Check to make sure Surf is actually in the database
		if Surf.is_saved(surf=surf):
			self.surfs.add(surf)
		
			# Save surfice object to database
			self.save()
	
	def add_surfs(self, surfs):
		""" Assign the surfice to additional surfs
			
			Adds on to any existing surfs this surfice might already
			be assigned to.
			Assumes the surfs already exist in the database.
			
			INPUT
			surfs		Array of surfs this surfice will be assigned to
		"""
		
		# Does NOT check if surfs are already in database (dangerous)
		# Expand the array out for .add()
		self.surfs.add(*surfs)
	
		# Save surfice object to database
		self.save()
	
	def set_description(self, description):
		""" Set the description of the surfice and save it to the database
			
			INPUT
			description		The new description of the surfice object
		"""
		
		# Set the description to the new description
		self.description = description
		
		# Save this object to the database
		self.save()
	
	def set_status(self, status, description='', event=True):
		""" Set the status of a surfice object
			
			INPUT
			status					a Status object
			description (optional)	The description of the status update
			event (optional)		Flag to create an event or not
		"""
		
		# If we want to create an event along with updating the status,
		# do it here.
		if event:
			Event.create(self, status, description)
		
		self.status = status
		self.save()
	
	def save_new(self, *args, **kwargs):
		""" Save a new surfice to the database
			
			This is useful if you created a surfice from scratch without
			using the create() method.  This will check to make sure the
			surfice doesn't already exist in the database, and if it
			doesn't, then save it to the database. From that point,
			you should use save().
			
			RETURNS
			True if saved successfully
			False if failed
		"""
		
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

	@staticmethod
	def is_saved(name=None, pk=None, surfice=None, exclude=-1):
		""" Check if a surfice is saved in the database
			
			This method checks by name, pk, or surfice.  If checking
			by name, you have a second option: to exclude a pk. This
			is useful when checking to see if a name exists in the
			database but you don't want to check the name of your current
			surfice (i.e. in form validation, you don't want to check if a surfice's
			own name exists in the database...we already know it does)
			
			INPUT
			name				Name of the surfice object
			pk					Private key of the surfice object
			surfice				Surfice object
			exclude (optional)	pk of surfice object that you want to exclude from name search
			
			RETURNS
			True if surfice is in database
			False if surfice is not in database
		"""
		
		exists = False
		
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


class Status(models.Model):
	""" Status class
		
		Dictates the status of a generic object...in our case a surfice
		
		CLASS VARIABLES
		name		Name of the status e.g. "Totally axed" or "choppy" or "clean"
		description	Description of the status
		data		Generic data
		
		METHODS
		Status		create(name, description)
		void		delete(self, *args, **kwargs)
		Status		get_status(name, pk, id)
		*Status		get_statuses(name)
		void		set(self, name, description, **kwargs)
		bool		set_name(self, name)
		void		set_description(self, description)
		bool		is_saved(name, pk, status)
	"""
	
	# Class variables
	name 		= models.CharField(max_length=512, unique=True)
	description = models.TextField(blank=True)
	data		= YAMLField()
	
	def __unicode__(self):
		""" Return the status name
		"""
		
		return self.name

	@staticmethod
	def create(name, description='', **kwargs):
		""" Create a new status and save it to the database
			
			INPUT
			name					Name of the status
			description (optional)	Description of the status
			**kwargs (optional)		Generic data to be put in the database
			
			RETURNS
			Status
		"""
		
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
	
	def delete(self, *args, **kwargs):
		""" Delete this status from the database
			
			INPUT
			*args, **kwargs		Only for extension of the built-in delete() function
		"""
		
		# Call the real delete() function
		super(Status, self).delete(*args, **kwargs)
	
	@staticmethod
	def get_status(name=None, pk=None, id=None):
		""" Get status by name or id
			
			If no parameters are passed, nothing is returned
			
			INPUT
			name (optional)		The name of the status
			id/pk (optional) 	The id/pk of the status
			
			RETURNS
			Status
			None if nothing is found
		"""
		
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
	
	@staticmethod
	def get_statuses(name=None):
		""" Get statuses by name or all
			
			INPUT
			name (optional)		Find statuses that contain this name
			
			RETURNS
			*Status
		"""
		
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
	
	def set(self, name=None, description=None, **kwargs):
		""" Set status components
			
			Generic setter function. All fields are optional, but
			nothing happens if no parameters are passed
			
			INPUT
			name (optional)			The new name of the status object
			description (optional)	The new description of the status object
			**kwargs				Generic data that goes in the data field
		"""
		
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
	
	def set_name(self, name):
		""" Set the name of the status to a new unique name
			
			Only set name if
			a) it's different
			b) it's not the same as another status (i.e. needs to be unique)
			
			RETURNS
			True if name change worked
			False if failed
		"""
		
		code = False
		
		# If you aren't changing the name, don't change it!
		if ' '.join(name.split()) == self.name:
			code = True
		
		# Check if new name already exists in database
		# If new name doesn't exist and isn't blank, set this object to that name	
		elif not Status.is_saved(name=name, exclude=self.id) and name.strip() != '':
			self.name = ' '.join(name.split())
			self.save()
			code = True
		
		return code
	
	def set_description(self, description):
		""" Set the description of the status
			
			INPUT
			description		The new description of the status object
		"""
		
		# Set the description to the new description
		self.description = description
		
		# Save this object to the database
		self.save()
	
	@staticmethod
	def is_saved(name=None, pk=None, status=None, exclude=-1):
		""" Check to see if status is in database
			
			This method checks by name, pk, or status.  If checking
			by name, you have a second option: to exclude a pk. This
			is useful when checking to see if a name exists in the
			database but you don't want to check the name of your current
			status (i.e. in form validation, you don't want to check if a status's
			own name exists in the database...we already know it does)
			
			INPUT
			name				Name of the status object
			pk					Private key of the object
			status				status object
			exclude (optional)	pk of status object to exclude from name search
			
			RETURNS
			True if Status object is in database
			False if Status object is not in database
		"""
		
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
	


class Ding(models.Model):
	""" Ding Class
		
		Any object of type Ding is an issue. This just captures the
		initial issue and the closing of the ding (issue).
		
		CLASS VARIABLES
		timestamp		timestamp of the original issue
		surfice			Which surfice is having the issue
		status			Status object the user is reporting
		email			Email of the user who submitted a ding
		description		Description of the ding
		data			Generic data stored as keys
		NEED RESOLVED FIELD
		
		METHODS
		Ding		create(surfice, status, email, description)
		Ding		get_ding(pk)
		*Ding		get_dings(...)
	"""
	
	# Class variables
	timestamp	= models.DateTimeField(auto_now=False, auto_now_add=True)
	surfice		= models.ForeignKey(Surfice)
	status		= models.ForeignKey(Status)
	email		= models.EmailField()
	description	= models.TextField(blank=True)
	data		= YAMLField()
	
	def __unicode__(self):
		""" Return the status name when referencing it directly
		"""
		
		return self.status.name
	
	@staticmethod
	def create(surfice, status, email, description='', **kwargs):
		""" Create a ding and save it in the database
			
			INPUT
			surfice					The surfice object that has a ding
			status					The reported status of the surfice
			email					The email address of the person who submitted the ding
			description (optional)	Description of the event
			**kwargs (optional)		Generic data stored as keys
			
			RETURNS
			Ding
		"""
		
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
	
	@staticmethod
	def get_ding(pk):
		""" Get ding by pk
			
			INPUT
			pk		primary key of the ding
			
			RETURNS
			Ding
			None if nothing is found
		"""
		
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
	
	@staticmethod
	def get_dings(**kwargs):
		""" Get dings based on arguments
			
			Get Dings in reverse chronological order after the optional
			order passed by the user.
			All arguments are optional, and only one at a time can be used
			(other than start/end arguments)
			If no argument is passed, all dings are returned
			
			INPUT
			dings			Number of dings to return
			surfice			Dings related this surfice
			email			Email address of the person who submitted the ding
			status			Reported status of the ding
			days			x number of days back from the current day to pull dings
			events			x number of dings to pull regardless of date
			start			timestamp (YYYY-MM-DD) of the start date of dings (inclusive)
			end				timestamp (YYYY-MM-DD) of the end date. Get dings
							from before and including this date.
			start, end		if both are set, all dings between (inclusive) will
							be returned
			[order, order_by,
			sort, sort_by]	Allows custom sorting, and then sorting by timestamp, then pk
			[none]			If no argument is passed, all stored dings will be returned
			
			RETURNS
			*Ding
		"""
		
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
		
		# Get this number of dings
		if 'dings' in kwargs:
			x = kwargs['dings']
			dings = Ding.objects.all().order_by(*order_by)[:x]
		
		# Get all dings related to a specific surfice
		elif 'surfice' in kwargs:
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



class Event(models.Model):
	""" Event Class
		
		A class for recording events of general objects
		and what the current status is.
		
		CLASS VARIABLES
		timestamp			timestamp of the event
		status				Status object
		surfice				Surfice object of the event
		description			Description of the event
		data				Generic data stored as keys
		
		METHODS
		Event			create(surfice, status, description)
		void			delete(self, *args, **kwargs)
		*Event			get_events(...)
		void			set(status, surfice, description, **kwargs)
	"""
	
	# Class variables
	timestamp	= models.DateTimeField(auto_now_add=True, auto_now=False)
	status		= models.ForeignKey(Status)
	surfice		= models.ForeignKey(Surfice)
	description	= models.TextField(blank=True)
	data		= YAMLField()
	
	def __unicode__(self):
		""" Return the status name when referencing it directly
		"""
		return self.status.name
	
	@staticmethod
	def create(surfice, status, description='', **kwargs):
		""" Create a new event and save it to the database
			
			INPUT
			surfice					The surfice object that has this event
			status					The status of the event
			description (optional)	Description of the event
			**kwargs (optional)		Generic data stored as keys
			
			RETURNS
			Event
		"""
		
		# Probably need to check these before setting them
		event = Event()
		
		# Set the event attributes
		event.surfice = surfice
		event.status = status
		event.description = description
		
		# Loop through kwargs and store as generic data in the database
		for key in kwargs:
			event.data[key] = kwargs[key]
		
		# Save the event in the database
		event.save()
		
		return event
	
	def delete(self, *args, **kwargs):
		""" Delete this event from the database
			
			INPUT
			*args, **kwargs		Only for extension of the built-in function
		"""
		
		# Call the real delete() function
		super(Event, self).delete(*args, **kwargs)
	
	@staticmethod
	def get_event(pk):
		""" Get event by id
			
			INPUT
			pk		Primary key of the Event
			
			RETURNS
			Event
			None if nothing is found
		"""
		
		# Default value to return is nothing
		event = None
		
		try:
			# If name is set, get the event that has that name
			event = Event.objects.get(pk=pk)
			
		# If nothing is found, do nothing
		except Event.DoesNotExist:
			pass
		
		return event
	
	@staticmethod
	def get_events(**kwargs):
		""" Get events by parameters passed
			
			Get events in reverse chronological order after the optional
			order passed by the user.
			All arguments are optional, and only one at a time can be used
			(other than start/end arguments)
			If no argument is passed, all events are returned
			
			INPUT
			days				x number of days back from the current day to pull events
			events				x number of events to pull regardless of date
			start				timestamp (YYYY-MM-DD) of the start date of events
			end					timestamp (YYYY-MM-DD) of the end date. Gets events
								from before and including this date
			start, end			if both are set, all events between (inclusive) will
								be returned.
			surfice				Surfice object that has events
			status				Status of events
			[order, order_by,
			sort, sort_by]		Allows custom sorting, and then sorting by
								timestamp, then pk
			[none]				If no argument is passed, all stored events will be returned
			
			RETURNS
			*Event
		"""
		
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
	
	def set(self, status=None, surfice=None, description=None, timestamp=None, **kwargs):
		""" Set components of event
			
			Generic setter function. All fields are optional, but
			nothing happens if no paramaters are passed
			
			INPUT
			status (optional)			The new name of the event
			surfice (optional)			The new surfice of the event
			description (optional)		The new description of the event
			timestamp (optional)		The new timestamp of the event
			**kwargs					Generic data stored as keys
		"""
		
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

