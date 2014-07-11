from surfice.models import Surf, Surfice, Status, Ding, Event
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import json
from django.forms.models import model_to_dict
from django.core import serializers

from surfice.serializers import *
from rest_framework.renderers import JSONRenderer

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
	try:
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
	except:
		# Surfice or status are not in the database
		pass
	
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
# update_event(request)
#
# Update an event's surfice, description, status, and data based on what's in request
# If no event is in request, nothing happens
#
# INPUT
# request						A request object
#	- pk						The pk of an event
#	- surfice (optional)		New name of the event
#	- description (optional)	New description of the event
#	- status (optional)			New status for the event
#	- data (optional)			JSON data for general data of the event
#
# RETURNS
# *errors
# -----------------------------------------
def update_event(request):
	errors = []
	
	# If status is set, go ahead and edit it
	if 'pk' in request.POST:
		post = {}
		
		# If using x-editable on the front side, convert the
		# confounded "name" attribute into the real one
		if 'name' in request.POST:
			post[request.POST['name']] = request.POST['value']
		else:
			post = request.POST
		
		# Get the status object
		event = Event.get_event(pk=request.POST['pk'])
		print post
		# If name is in request, give this status a new name
		# Returns a False flag when another status already has this new name
		if 'surfice' in post:
			flag = event.set( surfice=Surfice.get_surfice(pk=post['surfice']) )
			if not flag:
				errors.append("That surfice doesn't exist.")
		
		# If description is in request, set the description to this new description
		if 'description' in post:
			event.set(description=post['description'])
		
		if 'status' in post:
			flag = event.set(status=Status.get_status(pk=post['status']))
			if not flag:
				errors.append("That status doesn't exist.")
		
		# If data is in request, set the general data
		if 'data' in post:
			# Get the JSON data from POST
			data = json.loads(post['data'])
			
			# Set the general data by passing in data as keyword arguments
			event.set(**data)
		
	
	# If no status is set, throw an error
	else:
		errors.append("It's usually good to have a event to edit.")
	
	return errors

# -----------------------------------------
# submit_ding(request)
#
# Submit a ding based on the surfice, email, and state passed to it
#
# INPUT
# request						A request object
#	- surfice					The pk of a status
#	- email						Email address of the user submitting the ding
#	- description (optional)	Description of the ding
#	- status (optional)			The reported status of the surfice
#	- data (optional)			JSON data for general data of the status (like color)
#
# RETURNS
# *errors
# -----------------------------------------
def submit_ding(request):
	errors = []
	
	# If both surfice and email is set
	if 'surfice' in request.POST and 'email' in request.POST:
		try:
			# First see if the email address is actually an email address
			validate_email(request.POST['email'])
			
			# Get the surfice from the database
			surfice = Surfice.get_surfice(pk=request.POST['surfice'])
			
			# If no surfice exists, raise an exception
			if type(surfice) is not Surfice: raise Exception()
			
			# If data is in request, parse the data
			data = {}
			if 'data' in request.POST:
				# Get the JSON data from POST
				data = json.loads(request.POST['data'])
			
			ding = Ding.create(
				Surfice.get_surfice(pk=request.POST['surfice']),
				Status.get_status(pk=request.POST['status']),
				request.POST['email'],
				request.POST['description'],
				**data
			)
			
		except ValidationError:
			# The user entered an invalid email address
			errors.append("Hey, that's not a valid email address")
			pass
		except:
			errors.append("Whoa, something unexpected happened")
			pass
	
	return errors

# -----------------------------------------
# get_surf(request)
#
# Gets a surf based on the id/pk passed
#
# INPUT
# request		A request object
#	- surf		The pk of the surf
#
# RETURNS
# Surf
# -----------------------------------------
def get_surf(request):
	surf = {}
	
	# Both surf and surfice need to be in request
	if 'surf' in request.GET:
		# Get the surf object from the database
		surf = Surf.get_surf(pk=request.GET['surf'])
		
		# Convert the surf to a dictionary so that we can pass it back as JSON
		#surf = model_to_dict(surf)
		
		# Serialize the surf
		surf = SurfSerializer(surf)
		surf = JSONRenderer().render(surf.data)
	
	# If surf was not in the request, throw an error
	else:
		surf.append("A Surf was not passed")
	
	return surf

# -----------------------------------------
# get_surfs(request)
#
# Gets all surfs from the database
#
# INPUT
# request		A request object
# 
# RETURNS
# *Surf
# -----------------------------------------
def get_surfs(request):
	surfs = {}
	
	# Get the surf object from the database
	surfs = Surf.get_surfs()
	
	# Serialize the surf
	surfs = SurfSerializer(surfs)
	surfs = JSONRenderer().render(surfs.data)
	
	return surfs

# -----------------------------------------
# get_surfice(request)
#
# Gets a surfice based on the id/pk passed
#
# INPUT
# request		A request object
#	- surfice	The pk of the surf
#
# RETURNS
# Surfice
# -----------------------------------------
def get_surfice(request):
	surfice = {}
	
	# Surfice needs to be in request
	if 'surfice' in request.GET:
		# Get the surfice object from the database
		surfice = Surfice.get_surfice(pk=request.GET['surfice'])
		
		# Serialize the surfice
		surfice = SurficeSerializer(surfice)
		surfice = JSONRenderer().render(surfice.data)
	
	# If surf was not in the request, throw an error
	else:
		surfice.append("A Surf was not passed")
	
	return surfice

# -----------------------------------------
# get_surfice(request)
#
# Gets surfices based on the whichever parameter is passed
#
# INPUT
# request		A request object
#	- ***		The pk of the surf
#
# RETURNS
# Surf
# -----------------------------------------
def get_surfices(request):
	surfices = {}
	
	# Both surf and surfice need to be in request
	if 'surf' in request.GET:
		# Get the surf object from the database
		surf = Surf.get_surf(pk=request.GET['surf'])
		
		# Get all the surfices within that Surf
		surfices = surf.get_surfices()
		
		# Convert the surf to a dictionary so that we can pass it back as JSON
		#surfices = model_to_dict(surfices)
		#print surfices[0].status.data.color
		surfices = SurficeSerializer(surfices)
		surfices = JSONRenderer().render(surfices.data)
	
	# If surf was not in the request get all the surfices
	else:
		surfices = Surfice.get_surfices()
		surfices = SurficeSerializer(surfices)
		surfices = JSONRenderer().render(surfices.data)
	
	return surfices

# -----------------------------------------
# get_surfs_with_surfices(request)
#
# Gets surfices based on the whichever parameter is passed
#
# INPUT
# request		A request object
#	- ***		The pk of the surf
#
# RETURNS
# Surf
# -----------------------------------------
def get_surfs_with_surfices(request):
	#context_dict = {}
	surfs = {}
	
	# Exactly the same as views.surfs()...
	
	# Query for surfs and add them to context_dict
	surfs = Surf.get_surfs()
	
	# For each Surf, query for Surfices and add them to context_dict
	#for i, surf in enumerate(surfs):
		#surfs[i].surfices = SurficeSerializer(surf.get_surfices())
		
	
	# Query all the Surfices and add them to context_dict
	#surfice_list = Surfice.get_surfices()
	#context_dict['surfices'] = SurficeSerializer(surfice_list)
	
	# Both surf and surfice need to be in request
	# if False and 'surf' in request.GET:
# 		# Get the surf object from the database
# 		surf = Surf.get_surf(pk=request.GET['surf'])
# 		
# 		# Get all the surfices within that Surf
# 		surfices = surf.get_surfices()
# 		
# 		# Convert the surf to a dictionary so that we can pass it back as JSON
# 		#surfices = model_to_dict(surfices)
# 		#print surfices[0].status.data.color
# 		surfices = SurficeSerializer(surfices)
# 		surfices = JSONRenderer().render(surfices.data)
# 	
# 	# If surf was not in the request get all the surfices
# 	elif False:
# 		surfices = Surfice.get_surfices()
# 		surfices = SurficeSerializer(surfices)
# 		surfices = JSONRenderer().render(surfices.data)
	
	surfs = SurfWithSurficeSerializer(surfs)
	surfs = JSONRenderer().render(surfs.data)
	
	print surfs
	
	return surfs

# -----------------------------------------
# get_status(request)
#
# Gets a status based on the id/pk passed
#
# INPUT
# request		A request object
#	- status	The status of the surf
#
# RETURNS
# Status
# -----------------------------------------
def get_status(request):
	status = {}
	
	# Both surf and surfice need to be in request
	if 'status' in request.GET:
		# Get the surf object from the database
		status = Status.get_status(pk=request.GET['status'])
		
		# Convert the surf to a dictionary so that we can pass it back as JSON
		#status = model_to_dict(status)
		#status = serializers.serialize("json", [status])
		
		status = StatusSerializer(status)
		status = JSONRenderer().render(status.data)
	
	# If surf was not in the request, throw an error
	else:
		status.append("A Surf was not passed")
	
	return status

# -----------------------------------------
# get_statuses(request)
#
# Gets an array of all statuses
#
# INPUT
# request		A request object
#	- status	The status of the surf
#
# RETURNS
# Status
# -----------------------------------------
def get_statuses(request):
	statuses = {}
	
	# Get the surf object from the database
	statuses = Status.get_statuses()
	
	# Convert the surf to a dictionary so that we can pass it back as JSON
	#status = model_to_dict(status)
	#status = serializers.serialize("json", [status])
	
	statuses = StatusSerializer(statuses)
	statuses = JSONRenderer().render(statuses.data)
	
	return statuses

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
	response = {}
	
	# Set the status of a surfice
	if action == 'set-status':
		response = json.dumps(set_status(request))
	
	# Set all surfices in a surf to a status
	elif action == 'set-surf-status':
		response = json.dumps(set_surf_status(request))
	
	# Set the surf of a surfice
	elif action == 'set-surf':
		response = json.dumps(set_surf(request))
	
	# Update the surf's name and description
	elif action == 'update-surf':
		response = json.dumps(update_surf(request))
	
	# Update the surfice's name, description, and surf
	elif action == 'update-surfice':
		response = json.dumps(update_surfice(request))
	
	# Update the status's name, description, and color
	elif action == 'update-status':
		response = json.dumps(update_status(request))
	
	# Update event's surfice, description, or status
	elif action == 'update-event':
		response = json.dumps(update_event(request))
		print response
	
	# Submit a ding from the user
	elif action == 'submit-ding':
		response = json.dumps(submit_ding(request))
	
	# Get a single surf
	elif action == 'get-surf':
		response = get_surf(request)
	
	# Get all surfs
	elif action == 'get-surfs':
		response = get_surfs(request)
	
	# Get a single surfice
	elif action == 'get-surfice':
		response = get_surfice(request)
	
	# Get a set of surfices
	elif action == 'get-surfices':
		response = get_surfices(request)
	
	# Get surfs with surfices in them
	elif action == 'get-surfs-with-surfices':
		response = get_surfs_with_surfices(request)
	
	# Get a single status
	elif action == 'get-status':
		response = get_status(request)
	
	# Get all statuses
	elif action == 'get-statuses':
		response = get_statuses(request)
	
	else:
		response = ["No action called " + action]
	
	return HttpResponse(response, content_type='application/json')
