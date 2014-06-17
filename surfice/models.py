from django.db import models

# Create your models here.

# --------------
# Surf Class
# Group container for a set of Surfices
# --------------

class Surf(models.Model):
	# Class variables
	name = models.CharField(max_length=128, unique=True)
	description = models.CharField(unique=False)
	
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

class Surfice(models.Model):
	# Class variables
	name = models.CharField(unique=True)
	group = models.ForeignKey(Surf)
	description = models.CharField(unique=False)
	
	def __unicode__(self):
		return self.name


# Events Class

# Statuses Class (could be in a separate app)

# Issues Class (different app!)
# Includes information from users of services that they submit.
# Includes methods that handle the various tasks related to tickets