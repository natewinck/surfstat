from django.db import models

# Create your models here.



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





# --------------
# Surf Class
# Group container for a set of Surfices
# --------------

class Surf(models.Model):
	# Class variables
	name = models.CharField(max_length=512, unique=True)
	description = models.TextField()
	
	# Class methods
	def __unicode__(self):
		return self.name


# Surfice Class
# The main class. Contains information connected to various services
# that you run.  Each has the following class variables
#
# name			Name of the service. Needs to be unique within its
#				group
# group			Which Surf group this belongs to. Defaults to NULL
# description	Description of the service
# timestamp		Set automatically the first time the surfice is created

class Surfice(models.Model):
	# Class variables
	name 		= models.CharField(max_length=512, unique=True)
	surf 		= models.ForeignKey(Surf)
	description = models.TextField()
	timestamp	= models.DateField(auto_now=False, auto_now_add=True)
	
	# Status is part of the model
	status = models.ForeignKey(Status)
	
	def __unicode__(self):
		return self.name
	
	#def __init__(self):
	#	self.name = "Default"
	#	self.description = "Default description"
	#	self.group = Surf()
	


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
#
class Ding(models.Model):
	# Class variables
	name		= models.CharField(max_length=512, unique=False)
	timestamp	= models.DateField(auto_now=False, auto_now_add=True)
	surfice	= models.ForeignKey(Surfice)
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
	surfice	= models.ForeignKey(Surfice)
	description	= models.TextField()
	
	def __unicode__(self):
		return self.name

