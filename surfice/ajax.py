from surfice.models import Surf, Surfice, Status, Ding, Event
from django.http import HttpResponse
import json

# -----------------------------------------
# set_status(request)
#
# Sets the status of a surfice based on the request parameters
# 
# If no surfice or status is in request, nothing happens
#
# INPUT
# request						A request object
#	- surfice					The pk of the surfice
#	- status					The pk of the surf
#	- description (optional)	The description of the status update
#
# RETURNS
# *errors
# -----------------------------------------
def set_status(request):
	errors = []
	# If neither surfice nor status are present,
	# don't do anything
	if 'surfice' in request.POST and 'status' in request.POST:
		print "ELSE"
		# Get the surfice and status parameters to set the status of the surfice
		surfice = Surfice.get_surfice(pk=request.POST['surfice'])
		status = Status.get_status(pk=request.POST['status'])
		
		# Get the description. If no description was passed,
		# fill it in with the default value of the empty string
		# Using .get() allows for description not being set in POST
		description = request.POST.get('description','')
		
		surfice.set_status(status, description)
	
	else:
		errors.append("I need a Surfice and a Status in order to update the status.")
	
	return errors

# -----------------------------------------
# set_surf_status(request)
#
# Sets the status of all surfices belonging to a surf based on the request parameters
# 
# If no surf or status is in request, nothing happens
#
# INPUT
# request						A request object
#	- surf						The pk of the surf
#	- status					The pk of the status
#	- description (optional)	The description of the status update
#
# RETURNS
# *errors
# -----------------------------------------
def set_surf_status(request):
	errors = []
	
	# If neither surfice nor status are present,
	# don't do anything
	if 'surf' not in request.POST or 'status' not in request.POST:
		# Do nothing
		errors.append("To set a Surf, I need both a Surf and a Status.")
		pass
	else:
		# Get the surf and status parameters to set the status of the surfice
		surf = Surf.get_surf(pk=request.POST['surf'])
		status = Status.get_status(pk=request.POST['status'])
		
		# Get the description. If no description was passed,
		# fill it in with the default value of the empty string
		# Using .get() allows for description not being set in POST
		description = request.POST.get('description','')
		
		# Get all the surfices associated with this surf
		surfices = surf.get_surfices()
		
		# Now set the status for all the Surfices in this Surf
		for surfice in surfices:
			surfice.set_status(status, description)
	
	return errors

# -----------------------------------------
# set_surf(request)
#
# Sets the surf of a surfice
# If no surf or surfice is in request, nothing happens
#
# INPUT
# request		A request object
#	- surf		The pk of the surf
#	- surfice	The pk of the surfice
#
# RETURNS
# *errors
# -----------------------------------------
def set_surf(request):
	errors = []
	
	# Both surf and surfice need to be in request
	if 'surf' in request.POST and 'surfice' in request.POST:
		# Get both surfice and surf objects from the database
		surfice = Surfice.get_surfice(pk=request.POST['surfice'])
		surf = Surf.get_surf(pk=request.POST['surf'])
		
		# Set the surf
		surfice.set_surf(surf)
		errors.append("This actually isn't an error...just a test")
	
	# If either surf or surfice was not in the request, throw an error
	else:
		errors.append("A Surf or Surfice was not passed")
	
	return errors

# -----------------------------------------
# update_surf(request)
#
# Update a surf's name and description
# If no surf or surfice is in request, nothing happens
#
# INPUT
# request		A request object
#	- surf						The pk of a surf
#	- name (optional)			New name of the surf
#	- description (optional)	New description of the surf
#	- data (optional)			JSON data for general data of the surf
#
# RETURNS
# *errors
# -----------------------------------------
def update_surf(request):
	errors = []
	
	# If there is a surf in request, go ahead and edit it
	if 'surf' in request.POST:
		
		# Get the surf object
		surf = Surf.get_surf(pk=request.POST['surf'])
		
		#### Edit get so that it uses pk AND id
		
		# If name is in request, edit the name
		# If the name already exists in the database, throw an error
		if 'name' in request.POST:
			flag = surf.set_name(request.POST['name'])
			if not flag:
				errors.append("That name is already in the database")
		
		# If description is in request, set the description
		if 'description' in request.POST:
			surf.set_description(request.POST['description'])
		
		# If data is in request, set the general data
		if 'data' in request.POST:
			# Get the JSON data from POST
			data = json.loads(request.POST['data'])
			
			# Set the general data by passing in data as keyword arguments
			surf.set(**data)
	
	# If no surf is in request, throw an error
	else:
		errors.append("It's usually good to have a Surf to edit.")
	
	return errors

# -----------------------------------------
# update_surfice(request)
#
# Update a surfice's surf, name, and description based on what's in request
# If no surfice is in request, nothing happens
#
# INPUT
# request						A request object
#	- surfice					The pk of a surfice
#	- surf (optional)			The pk of a surf
#	- name (optional)			New name of the surfice
#	- description (optional)	New description of the surfice
#	- data (optional)			JSON data for general data of the surfice
#
# RETURNS
# *errors
# -----------------------------------------
def update_surfice(request):
	errors = []
	
	# If surfice is set, go ahead and edit it
	if 'surfice' in request.POST:
		
		# Get the surfice object
		surfice = Surfice.get_surfice(pk=request.POST['surfice'])
		
		# If surf is set in request, set this new surf to the surfice
		if 'surf' in request.POST:
			surfice.set_surf(Surf.get_surf(pk=request.POST['surf']))
		
		# If name is in request, give this surfice a new name
		# Returns a False flag when another surfice already has this new name
		if 'name' in request.POST:
			flag = surfice.set_name(request.POST['name'])
			if not flag:
				errors.append("That name is already being used by another Surfice.")
		
		# If description is in request, set the description to this new description
		if 'description' in request.POST:
			surfice.set_description(request.POST['description'])
		
		# If data is in request, set the general data
		if 'data' in request.POST:
			# Get the JSON data from POST
			data = json.loads(request.POST['data'])
			
			# Set the general data by passing in data as keyword arguments
			surfice.set(**data)
	
	# If no surfice is set, throw an error
	else:
		errors.append("It's usually good to have a Surfice to edit.")
	
	return errors

# -----------------------------------------
# update_status(request)
#
# Update a status's name, description, and color based on what's in request
# If no status is in request, nothing happens
#
# INPUT
# request						A request object
#	- status					The pk of a status
#	- name (optional)			New name of the status
#	- description (optional)	New description of the status
#	- data (optional)			JSON data for general data of the status (like color)
#
# RETURNS
# *errors
# -----------------------------------------
def update_status(request):
	errors = []
	
	# If status is set, go ahead and edit it
	if 'status' in request.POST:
		
		# Get the status object
		status = Status.get_status(pk=request.POST['status'])
		
		# If name is in request, give this status a new name
		# Returns a False flag when another status already has this new name
		if 'name' in request.POST:
			flag = status.set_name(request.POST['name'])
			if not flag:
				errors.append("That name is either already being used by another status, or you didn't change this one.")
		
		# If description is in request, set the description to this new description
		if 'description' in request.POST:
			status.set_description(request.POST['description'])
		
		# If data is in request, set the general data
		if 'data' in request.POST:
			# Get the JSON data from POST
			data = json.loads(request.POST['data'])
			
			# Set the general data by passing in data as keyword arguments
			status.set(**data)
	
	# If no status is set, throw an error
	else:
		errors.append("It's usually good to have a status to edit.")
	
	return errors

# -----------------------------------------
# dispatch(request, action)
#
# Fires functions based on the action passed.
# If no action is passed, nothing happens
#
# INPUT
# request				A request object
# action (optional)		A string that corresponds to a function
#
# ACTIONS
# set-status			Set status of surfice
# set-surf-status		Set status of an entire surf
# set-surf				Set surf of a surfice
# update-surf			Update info of surf
# update-surfice		Update info of surfice
#
# RETURNS
# HttpResponse
# -----------------------------------------
def dispatch(request, action=''):
	print "hello?"
	errors = {}
	
	# Set the status of a surfice
	if action == 'set-status':
		errors = set_status(request)
	
	# Set all surfices in a surf to a status
	elif action == 'set-surf-status':
		errors = set_surf_status(request)
	
	# Set the surf of a surfice
	elif action == 'set-surf':
		errors = set_surf(request)
	
	# Update the surf's name and description
	elif action == 'update-surf':
		errors = update_surf(request)
	
	# Update the surfice's name, description, and surf
	elif action == 'update-surfice':
		errors = update_surfice(request)
	
	# Update the status's name, description, and color
	elif action == 'update-status':
		errors = update_status(request)
	
	else:
		errors = ["No action called " + action]
	
	return HttpResponse(json.dumps(errors), content_type='application/json')
