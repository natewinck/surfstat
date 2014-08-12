# Import the models and their serializers
from surfice.models import Surf, Surfice, Status, Ding, Event
from surfice.serializers import (SurfSerializer, SurficeSerializer, StatusSerializer,
	EventSerializer, DingSerializer)

# Import json renderers
from rest_framework.renderers import JSONRenderer
import json

# Import form validation
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# Import date and time
import time
from datetime import datetime

# Import url helpers
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from surfice import views

# Import authentication
from django.contrib.auth.decorators import permission_required

# Import reverse so we can build urls
from django.core.urlresolvers import reverse

# Import the response so we can return
from django.http import HttpResponse


@permission_required('is_superuser', raise_exception=True)
def set_status(request):
	""" Sets the status of a surfice
	
		If no surfice or status is in the request, nothing happens.
		
		INPUT
		request.POST
			- surfice					The pk of the surfice
			- status					The pk of the surf
			- description (optional)	The description of the status update
		
		RETURNS
		*errors
	"""
	
	errors = []
	# If neither surfice nor status are present,
	# don't do anything
	try:
		if 'surfice' in request.POST and 'status' in request.POST:
			#print "ELSE"
			# Get the surfice and status parameters to set the status of the surfice
			surfice = Surfice.get_surfice(pk=request.POST['surfice'])
			status = Status.get_status(pk=request.POST['status'])
		
			# Get the description. If no description was passed,
			# fill it in with the default value of the empty string
			# Using .get() allows for description not being set in POST
			description = request.POST.get('description','')
			
			# If event is set and is set to False, don't create an event with the update
			if 'event' in request.POST and int(request.POST['event']) == 0:
				event = False
			# Create an event by default
			else:
				event = True
			
			# Set the status of the surf, which also creates an event
			surfice.set_status(status, description, event=event)
	
		else:
			errors.append("I need a Surfice and a Status in order to update the status.")
	except:
		# Surfice or status are not in the database
		pass
	
	return errors

@permission_required('is_superuser', raise_exception=True)
def set_surf_status(request):
	""" Sets the status of all surfices belonging to a surf.
		
		If no surf or status is in request, nothing happens.
		
		INPUT
		request						A request object
			- surf						The pk of the surf
			- status					The pk of the status
			- description (optional)	The description of the status update
			- all (optional)			Flag for setting all surfs instead of only one
			- event (optional)			Flag for creating an event or not
		
		RETURNS
		*errors
	
	"""
	errors = []
	
	# Set the status of all surfs
	if 'all' in request.POST and 'status' in request.POST:
		# Get all the surfices
		surfices = Surfice.get_surfices()
		
		# Get the status that all the surfices will be set to
		status = Status.get_status(pk=request.POST['status'])
		
		# Get the description. If no description was passed,
		# fill it in with the default value of the empty string
		# Using .get() allows for description not being set in POST
		description = request.POST.get('description','')
		
		# If event is set and is set to False, don't create an event with the update
		if 'event' in request.POST and int(request.POST['event']) == 0:
			event = False
		# Create an event by default
		else:
			event = True
		
		# Now set the status for all the Surfices in this Surf
		for surfice in surfices:
			surfice.set_status(status, description, event=event)
	
	# Set the status of a specific surf
	elif 'surf' in request.POST and 'status' in request.POST:
		# Get the surf and status parameters to set the status of the surfice
		surf = Surf.get_surf(pk=request.POST['surf'])
		status = Status.get_status(pk=request.POST['status'])
		
		# Get the description. If no description was passed,
		# fill it in with the default value of the empty string
		# Using .get() allows for description not being set in POST
		description = request.POST.get('description','')
		
		# If event is set and is set to False, don't create an event with the update
		if 'event' in request.POST and int(request.POST['event']) == 0:
			event = False
		# Create an event by default
		else:
			event = True
		
		# Get all the surfices associated with this surf
		surfices = surf.get_surfices()
		
		# Now set the status for all the Surfices in this Surf
		for surfice in surfices:
			surfice.set_status(status, description, event=event)
		
	# If none of the previous conditions is met,
	# don't do anything
	else:
		# Do nothing
		errors.append("To set a Surf, I need both a Surf and a Status. If setting all Surfs, I need a Status.")
		pass
	
	
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
#	- surfices	Array of pks of surfices
#
# RETURNS
# *errors
# -----------------------------------------
@permission_required('is_superuser', raise_exception=True)
def set_surf(request):
	errors = []
	
	# Both surf and surfice need to be in request
	if 'surf' in request.POST and 'surfice' in request.POST:
		# Get both surfice and surf objects from the database
		surfice = Surfice.get_surfice(pk=request.POST['surfice'])
		surf = Surf.get_surf(pk=request.POST['surf'])
		
		# Set the surf
		surfice.set_surf(surf)
	
	elif 'surf' in request.POST and 'surfices' in request.POST:
		# Get the surf object from the database
		surf = Surf.get_surf(pk=request.POST['surf'])
		
		# Get the surfice objects based on the pks that were passed
		surfices = []
		# Loop through the passed pks and append the surf to surfs array
		for pk in request.POST.getlist('surfices'):
			surfices.append( Surfice.get_surfice(pk=pk) )
		
		# Now set these surfices to the surf
		surf.surfices = surfices
	
	# If only surf is set, clear all the surfices from the surf
	elif 'surf' in request.POST:
		# Get the surf object from the database
		surf = Surf.get_surf(pk=request.POST['surf'])
		
		# Clear the surfices from this surf
		surf.surfices.clear()
	
	# If either surf or surfice was not in the request, throw an error
	else:
		errors.append("A Surf or Surfice was not passed")
	
	return errors

@permission_required('is_superuser', raise_exception=True)
def set_surfs(request):
	""" Sets the surfs of a surfice
		
		If no surfs or surfice are in request, nothing happens
		
		INPUT
		request			A request object
			- surfs		Array of pks of surfs
			- surfice	The pk of the surfice
		
		RETURNS
		*errors
	"""
	errors = []
	
	# Both surf and surfice need to be in request
	if 'surfs' in request.POST and 'surfice' in request.POST:
		# Get both surfice and surf objects from the database
		surfice = Surfice.get_surfice(pk=request.POST['surfice'])
		surf = Surf.get_surf(pk=request.POST['surf'])
		
		# Get the surf objects based on the pks that were passed.
		# Loop through the passed pks and append the surf to surfs array
		surfs = []
		for pk in request.POST.getlist('surfs'):
			surfs.append( Surf.get_surf(pk=pk) )
		
		# Set the surfs of the surfice, replacing any that were already there
		surfice.set_surfs(surfs)
	
	# If either surf or surfice was not in the request, throw an error
	else:
		errors.append("A Surf or Surfice was not passed")
	
	return errors

@permission_required('is_superuser', raise_exception=True)
def add_surf(request):
	""" Add a surf to a surfice
		
		If no surf or surfice is in request, nothing happens
		
		INPUT
		request			A request object
			- surf		The pk of the surf
			- surfice	The pk of the surfice
		
		RETURNS
		*errors
	"""
	errors = []
	
	# Both surf and surfice need to be in request
	if 'surf' in request.POST and 'surfice' in request.POST:
		# Get both surfice and surf objects from the database
		surfice = Surfice.get_surfice(pk=request.POST['surfice'])
		surf = Surf.get_surf(pk=request.POST['surf'])
		
		# Add the surf to the surfice
		surfice.add_surf(surf)
	
	# If either surf or surfice was not in the request, throw an error
	else:
		errors.append("A Surf or Surfice was not passed")
	
	return errors

@permission_required('is_superuser', raise_exception=True)
def add_surfs(request):
	""" Add surfs to a surfice
		
		If no surfs or surfice are in request, nothing happens
		
		INPUT
		request			A request object
			- surfs		Array of pks of surfs
			- surfice	The pk of the surfice
		
		RETURNS
		*errors
	"""
	
	errors = []
	
	# Both surf and surfice need to be in request
	if 'surfs' in request.POST and 'surfice' in request.POST:
		# Get both surfice and surf objects from the database
		surfice = Surfice.get_surfice(pk=request.POST['surfice'])
		surf = Surf.get_surf(pk=request.POST['surf'])
		
		# Get the surf objects based on the pks that were passed.
		# Loop through the passed pks and append the surf to surfs array
		surfs = []
		for pk in request.POST.getlist('surfs'):
			surfs.append( Surf.get_surf(pk=pk) )
		
		# Add the surfs to the surfice
		surfice.add_surfs(surfs)
	
	# If either surf or surfice was not in the request, throw an error
	else:
		errors.append("A Surf or Surfice was not passed")
	
	return errors

@permission_required('is_superuser', raise_exception=True)
def update_surf(request):
	""" Update a surf's attributes
		
		If no surf is in request, nothing happens.
		
		INPUT
		request							A request object
			- surf						The pk of a surf
			- name (optional)			The new name of the surf
			- description (optional)	New description of the surf
			- data (optional)			JSON data for general data of the surf
		
		RETURNS
		*errors
	"""
	
	errors = []
	
	# If there is a surf in request, go ahead and edit it
	if 'surf' in request.POST:
		
		# Get the surf object
		surf = Surf.get_surf(pk=request.POST['surf'])
		
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

@permission_required('is_superuser', raise_exception=True)
def update_surfice(request):
	""" Update a surfice's attributes
		
		If no surfice is in request, nothing happens
		
		INPUT
		request							A request object
			- surfice					The pk of a surfice
			- surf (optional)			The pk of a surf
			- surfs (optional)			pks of surfs
			- name (optional)			New name of the surfice
			- description (optional)	New description of the surfice
			- data (optional)			JSON data for general data of the surfice
		
		RETURNS
		*errors
	"""
	
	errors = []
	
	# If surfice is set, go ahead and edit it
	if 'surfice' in request.POST:
		
		# Get the surfice object
		surfice = Surfice.get_surfice(pk=request.POST['surfice'])
		
		# If surf is set in request, set this new surf to the surfice
		if 'surf' in request.POST:
			# If surf is -1, that means we need to clear the surfs from the surfice
			if int( request.POST['surf'] ) == -1:
				surfice.surfs.clear()
			
			# If surf is set to a real surf, set the surfice's surf to that
			else:
				surfice.set_surf(Surf.get_surf(pk=request.POST['surf']))
		
		# Surfs is set in request, set this new surf to the surfice
		elif 'surfs' in request.POST:
			# Get the surf objects based on the pks that were passed
			surfs = []
			# If surfs were set in the request add them to the array
			if 'surfs' in request.POST:
				# Loop through the passed pks and append the surf to surfs array
				for pk in request.POST.getlist('surfs'):
					surfs.append( Surf.get_surf(pk=pk) )
		
			# Set the surfs of the surfice
			surfice.set_surfs(surfs)
		
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
			print data
			
			# Set the general data by passing in data as keyword arguments
			surfice.set(**data)
	
	# If no surfice is set, throw an error
	else:
		errors.append("It's usually good to have a Surfice to edit.")
	
	return errors

@permission_required('is_superuser', raise_exception=True)
def update_status(request):
	""" Update a status's attributes
		
		If no status is in request, nothing happens
		
		INPUT
		request						A request object
			- status					The pk of a status
			- name (optional)			New name of the status
			- description (optional)	New description of the status
			- data (optional)			JSON data for general data of the status (like color)
		
		RETURNS
		*errors
	"""
	
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

@permission_required('is_superuser', raise_exception=True)
def update_event(request):
	""" Update an event's attribute
		If no event is in request, nothing happens
		
		INPUT
		request							A request object
			- pk						The pk of an event
			- surfice (optional)		New name of the event
			- description (optional)	New description of the event
			- status (optional)			New status for the event
			- data (optional)			JSON data for general data of the event
		
		RETURNS
		*errors
	"""
	
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
		
		# If surfice is in request, assign this event to this new surfice
		if 'surfice' in post:
			flag = event.set( surfice=Surfice.get_surfice(pk=post['surfice']) )
			if not flag:
				errors.append("That surfice doesn't exist.")
		
		# If description is in request, set the description to this new description
		if 'description' in post:
			event.set(description=post['description'])
		
		# If status is in request, set the event to the new status
		if 'status' in post:
			flag = event.set(status=Status.get_status(pk=post['status']))
			if not flag:
				errors.append("That status doesn't exist.")
		
		if 'timestamp' in post:
			# Timestamp passed in format "01/21/2012 14:30:59"
			strp_time = time.strptime(post['timestamp'], "%m/%d/%Y %H:%M:%S")
			
			# Convert the time to a Django-acceptable timestamp
			date_django = datetime.fromtimestamp(time.mktime(strp_time))
			
			# Set the timestamp
			event.set(timestamp=date_django)

		
		# If data is in request, set the general data
		if 'data' in post:
			# Get the JSON data from POST
			data = json.loads(post['data'])
			
			# Set the general data by passing in data as keyword arguments
			event.set(**data)
		
	
	# If no status is set, throw an error
	else:
		errors.append("It's usually good to have an event to edit.")
	
	return errors

@permission_required('is_superuser', raise_exception=True)
def delete_surf(request):
	""" Delete a surf
		
		INPUT
		request			A request object
			- surf		The pk of a surf
			- delete	The flag to delete
		
		RETURNS
		*errors
	"""
	errors = []
	
	# If surf and delete are set, go ahead and delete the surf
	if	(
				'delete' in request.POST and
				'surf' in request.POST
			):
			
			# Get the surf that we're about to delete
			surf = Surf.get_surf(pk=request.POST['surf'])
			
			# Check to make sure this is a real Surf object, then delete it
			if type(surf) is Surf:
				surf.delete()
		
	
	# If no surf is set, throw an error
	else:
		errors.append("It's usually good to have a surf to delete.")
	
	return errors

@permission_required('is_superuser', raise_exception=True)
def delete_surfice(request):
	""" Delete a surfice
		
		INPUT
		request			A request object
			- surfice	The pk of a surfice
			- delete	The flag to delete
		
		RETURNS
		*errors
	"""
	errors = []
	
	# If surfice and delete are set, go ahead and delete the surfice
	if	(
				'delete' in request.POST and
				'surfice' in request.POST
			):
			
			# Get the surfice that we're about to delete
			surfice = Surfice.get_surfice(pk=request.POST['surfice'])
			
			# Check to make sure this is a real Surfice object, then delete it
			if type(surfice) is Surfice:
				surfice.delete()
		
	
	# If no surfice is set, throw an error
	else:
		errors.append("It's usually good to have a surfice to delete.")
	
	return errors

@permission_required('is_superuser', raise_exception=True)
def delete_status(request):
	""" Delete a status
		
		INPUT
		request			A request object
			- status	The pk of a status
			- delete	The flag to delete
		
		RETURNS
		*errors
	"""
	errors = []
	
	# If status and delete are set, go ahead and delete the status
	if	(
				'delete' in request.POST and
				'status' in request.POST
			):
			
			# Get the status that we're about to delete
			status = Status.get_status(pk=request.POST['status'])
			
			# Check to make sure this is a real Surf object, then delete it
			if type(status) is Status:
				status.delete()
		
	
	# If no status is set, throw an error
	else:
		errors.append("It's usually good to have a status to delete.")
	
	return errors

@permission_required('is_superuser', raise_exception=True)
def delete_event(request):
	""" Delete an event
		
		INPUT
		request			A request object
			- event		The pk of an event
			- delete	The flag to delete
		
		RETURNS
		*errors
	"""
	errors = []
	
	# If event and delete are set, go ahead and delete the event
	if	(
				'delete' in request.POST and
				'event' in request.POST
			):
			
			# Get the event that we're about to delete
			event = Event.get_event(pk=request.POST['event'])
			
			# Check to make sure this is a real Event object, then delete it
			if type(event) is Event:
				event.delete()
		
	
	# If no event is set, throw an error
	else:
		errors.append("It's usually good to have an event to delete.")
	
	return errors

@permission_required('is_superuser', raise_exception=True)
def delete_ding(request):
	""" Delete a ding
		
		INPUT
		request			A request object
			- ding		The pk of a ding
			- delete	The flag to delete
		
		RETURNS
		*errors
	"""
	errors = []
	
	# If ding and delete are set, go ahead and delete the ding
	if	(
				'delete' in request.POST and
				'ding' in request.POST
			):
			
			# Get the surfice that we're about to delete
			ding = Ding.get_ding(pk=request.POST['ding'])
			
			# Check to make sure this is a real Ding object, then delete it
			if type(ding) is Ding:
				ding.delete()
		
	
	# If no ding is set, throw an error
	else:
		errors.append("It's usually good to have a ding to delete.")
	
	return errors

def submit_ding(request):
	""" Submit a ding for a surfice
		
		INPUT
		request							A request object
			- surfice					The pk of a surfice
			- email						Email address of the user submitting the ding
			- description (optional)	Description of the ding
			- status				The reported status of the surfice
			- data (optional)			JSON data for general data of the ding
		
		RETURNS
		*errors
	"""
	errors = []
	
	# If both surfice, email, and status are set
	if (
			'surfice'	in request.POST and
			'email' 	in request.POST and
			'status' 	in request.POST
		):
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
			
			#print "DATA:"
			#print data
			#data = json.JSONDecoder()
			
			# Add in user agent data
			from user_agents import parse
			
			# Get the data and parse it
			ua_string = request.META['HTTP_USER_AGENT']
			user_agent = parse(ua_string)
			
			# Accessing user agent's browser attributes
			data['browser'] = {
				#'original': user_agent.browser, # returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')
				'family': user_agent.browser.family, # returns 'Mobile Safari'
				'version': user_agent.browser.version, # returns (5, 1)
				'version_string': user_agent.browser.version_string # returns '5.1'
			}

			# Accessing user agent's operating system properties
			data['os'] = {
				#'original': user_agent.os,  # returns OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')
				'family': user_agent.os.family,  # returns 'iOS'
				'version': user_agent.os.version,  # returns (5, 1)
				'version_string': user_agent.os.version_string  # returns '5.1'
			}
	
			# Accessing user agent's device properties
			data['device'] = {
				#'original': user_agent.device,  # returns Device(family='iPhone')
				'family': user_agent.device.family #returns 'iPhone'
			}
			
			data['hostname'] = request.META.get('REMOTE_HOST')
			data['ip'] = request.META['REMOTE_ADDR']
			
			#print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
			
			# Create the ding
			ding = Ding.create(
				surfice,
				Status.get_status(pk=request.POST['status']),
				request.POST['email'],
				request.POST.get('description', ''),
				**data
			)
			
			# Now that we've created the ding, push the information to a syslog
			#2.190 standard 514 udp
			
		except ValidationError:
			# The user entered an invalid email address
			errors.append("Hey, that's not a valid email address")
			pass
		#except:
			#errors.append("Whoa, something unexpected happened")
			#pass
	
	# If no surfice is set, throw an error
	else:
		errors.append("It's usually good to have a surfice to assign a ding to.")
	
	return errors

@permission_required('is_superuser', raise_exception=True)
def send_email(request):
	"""	Send an email
		
		Will not only send to a specific address, but will also
		send to cc, and bcc fields.
		
		INPUT
		request
			- to				To field
			- from (optional)	From field
			- cc (optional)		CC field
			- bcc (optional)	BCC field
			- subject			Subject field
			- body				Body of email
	"""
	if	(
			'to' 		in request.POST and
			'subject' 	in request.POST and
			'body'		in request.POST
		):
		
		try:
			# First see if the email address is actually an email address
			validate_email(request.POST['to'])
			
			# Start creating the EmailMessage object
			email = EmailMessage(to=[request.POST['to']], subject=request.POST['subject'], body=request.POST['body'])
			
			if 'from' in request.POST:
				email.from_email = request.POST['from']
			
			if 'cc' in request.POST:
				email.cc = request.POST['cc']
			
			if 'bcc' in request.POST:
				email.bcc = request.POST['bcc']
			
			# Now actually mail the email
			#from django.core import mail
			#connection = mail.get_connection()
			
			email.send()
			
		except ValidationError:
			pass

@permission_required('is_superuser', raise_exception=True)
def submit_rt_ticket(request):
	""" Submit an RT ticket by email
		
		INPUT
		request
			- requestor (optional)		Requestor email address
			- queue						Queue email address
			- body						Body of the RT ticket
			- name (optional)			Name in the subject line
			- phone	(optional)			phone number in the subject line
			- location (optional)		location in the subject line
			- description (optional)	brief description in the subject line
	"""
	if	(
			'queue'		in request.POST and
			'body'		in request.POST
		):
		try:
			
			# Create the subject line
			subject = ''
		
			if 'name' in request.POST and request.POST['name'] != '':
				subject += request.POST['name'] + ' - '
		
			if 'phone' in request.POST and request.POST['phone'] != '':
				subject += request.POST['phone'] + ' - '
		
			if 'location' in request.POST and request.POST['location'] != '':
				subject += request.POST['location'] + ' - '
		
			if 'description' in request.POST and request.POST['description'] != '':
				subject += request.POST['description']
			else:
				subject += 'Network Issue'
			
			# Get the requestor from POST if set
			print "requestor: "
			if 'requestor' in request.POST:
				validate_email(request.POST['requestor'])
				requestor = request.POST['requestor']
			
			# If it's not set, get it from the settings file
			else:
				from surfstat.settings import EMAIL_HOST_USER
				requestor = EMAIL_HOST_USER
			
			print requestor
			
			# Remove extra spaces from the subject
			subject = ' '.join(subject.split())
			
			# Add a space to each new line of the body
			lines = request.POST['body'].split('\n')
			body = ''
			for line in lines:
				body += ' ' + line + '\n'
			body = body.strip()
			
			print ''
			print body
			print ''
			print lines
			print ''
			
			#for line in request.POST['body']:
			#	 body = ('%s%s%s\n' % (body, ' ', line.rstrip('\n')))
			
			# To send data to RT, we need to put everything in a
			# variable named RT, with keys and values on separate lines.
			# Multiple lines will be indented
			content =(	'id: ticket/new\n'
						'Queue: ' + request.POST['queue'] + '\n'
						'Requestor: ' + requestor + '\n'
						'Subject: ' + subject + '\n'
						'Text: ' + body + '\n'
					)
			
			import urllib, urllib2
			from surfstat.settings import RT_HOST, RT_USER, RT_PASSWORD
			print RT_HOST, RT_USER, RT_PASSWORD
			post = [('user', RT_USER), ('pass', RT_PASSWORD), ('content', content),]
			
			result = urllib2.urlopen( RT_HOST, urllib.urlencode(post) )
			
			#print 'RESULT:'
			#print result.read()
			
			return result.read()
			
			#from django.core.mail import send_mail
			# Start creating the EmailMessage object
			#email = EmailMessage(
			#send_mail(
			#			from_email=requestor,
			#			recipient_list=[request.POST['queue']],
			#			subject=subject,
			#			message=request.POST['body'])
			
			# Now actually send the email
			#email.send()
			
		except ValidationError:
			pass

@permission_required('is_superuser', raise_exception=True)
def get_surf(request):
	""" Get a surf by name or id
		
		INPUT
		request			A request object
			- surf		The pk of the surf
			- name		The name of the surf
		
		RETURNS
		Surf
	"""
	
	surf = {}
	
	# If surf is set, get a surf object by id
	if 'surf' in request.GET:
		# Get the surf object from the database
		surf = Surf.get_surf(pk=request.GET['surf'])
		
		# Serialize the surf
		surf = SurfSerializer(surf)
		surf = JSONRenderer().render(surf.data)
	
	# If name is set, get a surf object by name
	elif 'name' in request.GET:
		# Get the surf object from the database
		surf = Surf.get_surf(name=request.GET['name'])
		
		# Serialize the surf
		surf = SurfSerializer(surf)
		surf = JSONRenderer().render(surf.data)
	
	# If surf or name were not in the request, throw an error
	else:
		surf.append("A Surf was not passed")
	
	return surf

@permission_required('is_superuser', raise_exception=True)
def get_surfs(request):
	""" Get surfs as JSON data
		
		If a parameter is set, get surfs by that.
		Otherwise, get all the surfs
		
		INPUT
		request			A request object
			- name		The name of the surf
		
		RETURNS
		*Surf
	"""
	
	surfs = {}
	
	# If name is set, get all the surfs that contain this name
	if 'name' in request.GET:
		# Get the surf objects that contain this name
		surfs = Surf.get_surfs(name=request.GET['name']).order_by('name')
	
	# If nothing is set, get all the surfs
	else:	
		# Get the surf object from the database
		surfs = Surf.get_surfs().order_by('name')
	
	# Serialize the surfs
	surfs = SurfSerializer(surfs)
	surfs = JSONRenderer().render(surfs.data)
	
	return surfs

@permission_required('is_superuser', raise_exception=True)
def get_surfice(request):
	""" Get a surfice by name or id
		
		INPUT
		request			A request object
			- surfice	The pk of the surfice
			- name		The name of the surfice
		
		RETURNS
		Surfice
	"""
	
	surfice = {}
	
	# If surfice is set, get the surfice by id
	if 'surfice' in request.GET:
		# Get the surfice object from the database
		surfice = Surfice.get_surfice(pk=request.GET['surfice'])
		
		# Serialize the surfice
		surfice = SurficeSerializer(surfice)
		surfice = JSONRenderer().render(surfice.data)
	
	# If name is set, get the surfice by name
	elif 'name' in request.GET:
		# Get the surfice object from the database
		surfice = Surfice.get_surfice(name=request.GET['name'])
		
		# Serialize the surfice
		surfice = SurficeSerializer(surfice)
		surfice = JSONRenderer().render(surfice.data)
		
	# If surf was not in the request, throw an error
	else:
		surfice.append("A Surf was not passed")
	
	return surfice

@permission_required('is_superuser', raise_exception=True)
def get_surfices(request):
	""" Get surfices by surf or all
		
		INPUT
		request			A request object
			- surf		The pk of the surf that surfices belong to
			- name		Get all surfices that contain this name
			- status	Get all surfices that have this status
			- [none]	Get all surfices
		
		RETURNS
		*Surfice
	"""
	
	surfices = {}
	
	# If surf is in request, get all the surfices that belong to it
	if 'surf' in request.GET:
		# Get the surf object from the database
		surf = Surf.get_surf(pk=request.GET['surf'])
		
		# Get all the surfices within that Surf
		surfices = surf.get_surfices().order_by('name')
	
	# If name is set, get all surfices that contain this name
	elif 'name' in request.GET:
		# Get all the surfices within that Surf
		surfices = surf.get_surfices(name=request.GET['name']).order_by('name')
	
	# If status is set, get all surfices that have this status
	elif 'status' in request.GET:
		# Get the status
		status = Status.get_status(pk=request.GET['status'])
		
		# Get all the surfices with that status
		surfices = Surfice.get_surfices(status=status).order_by('name')
	
	# If nothing was set in GET, get all the surfices
	else:
		surfices = Surfice.get_surfices().order_by('name')
	
	# Serialize the surfices so that we can pass them back as an array of JSON objects
	surfices = SurficeSerializer(surfices)
	surfices = JSONRenderer().render(surfices.data)
	
	return surfices

@permission_required('is_superuser', raise_exception=True)
def get_status(request):
	""" Get a status by id or name
		
		INPUT
		request			A request object
			- status	The status id
			- name		The name of the status
		
		RETURNS
		Status
	"""
	
	status = {}
	
	# If status is set, get the status object by id
	if 'status' in request.GET:
		# Get the status object from the database
		status = Status.get_status(pk=request.GET['status'])
		
		# Serialize the status so that we can pass it back as JSON
		status = StatusSerializer(status)
		status = JSONRenderer().render(status.data)
	
	# If name is set, get the status object by name
	elif 'name' in request.GET:
		# Get the status object from the database
		status = Status.get_status(name=request.GET['name'])
		
		# Serialize the status so that we can pass it back as JSON
		status = StatusSerializer(status)
		status = JSONRenderer().render(status.data)
	
	# If nothing was set, throw an error
	else:
		status.append("A Status id or name was not passed")
	
	return status

@permission_required('is_superuser', raise_exception=True)
def get_statuses(request):
	""" Get an array of statuses
		
		If no parameters are set, get all the statuses
		
		INPUT
		request			A request object
			- name		Get all statuses that contain this name
		
		RETURNS
		*Status
	"""
	
	statuses = {}
	
	# If name is set, get all statuses that contain this name
	if 'name' in request.GET:
		statuses = Status.get_statuses(name=request.GET['name'])
	
	# If nothing is set, get all statuses
	else:
		# Get the status object from the database
		statuses = Status.get_statuses()
	
	# Serialize the status so that we can pass it back as JSON
	statuses = StatusSerializer(statuses)
	statuses = JSONRenderer().render(statuses.data)
	
	return statuses

@permission_required('is_superuser', raise_exception=True)
def get_event(request):
	""" Get an event
		
		This will either get event by id
		or get the first/last event of a page
		based on pagination settings in views.py
		
		INPUT
		request				A request object
			- event			The pk of the event
			- page			The pagination page of the event
			- first, last	Get the first or last event on the page
		
		RETURNS
		Event
	"""
	
	event = {}
	
	# The event pk needs to be in request
	if 'event' in request.GET:
		# Get the event object from the database
		event = Event.get_event(pk=request.GET['event'])
		
		event = EventSerializer(event)
		event = JSONRenderer().render(event.data)
	
	elif 'page' in request.GET:
		# For ease of use, get the page
		page = request.GET['page']
	
		# Initialize paginator
		# 10 per page - references what is in views.py
		events = Event.get_events()
		paginator = Paginator(events, 10)
	
		# Fill the events array with the current page
		try:
			events_page = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver the first page
			events_page = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver the last page of events
			events_page = paginator.page(paginator.num_pages)
		
		if 'first' in request.GET:
			event = events[0]
		elif 'last' in request.GET:
			event = events[events_page.end_index()-1]
		
		event = EventSerializer(event)
		event = JSONRenderer().render(event.data)
	
	# If event or page were not in the request, throw an error
	else:
		event.append("An event or page was not passed")
	
	return event

@permission_required('is_superuser', raise_exception=True)
def get_events(request):
	""" Get an array of events
		
		Only one order_by and one get mode can be used at a time.
		For example, I can order by timestamp, over a certain number of days
		
		INPUT
		request			A request object
			- days				int in number of days back from the current day to pull events
			- events			int number of events to pull regardless of date
			- start				timestamp (YYYY-MM-DD) of the start date of events
			- end				timestamp (YYYY-MM-DD) of the end date. Gets events
			-					from before and including this date
			- start, end		if both are set, all events between (inclusive)
			-					will be returned
			- surfice			Surfice object that has events
			- status			Status of events
			- [sort, sort_by,
			- order, order_by] 	Allows custom sorting, and then sorting by
			-					timestamp and then pk
			- [none]			If no argument is passed, all stored events will be returned
			-
			- RETURNS
			- Array of events in reverse chronological order (newest first)
		
		RETURNS
		*Event in order_by order or reverse chronological order (newest first)
	"""
	
	events = {}
	
	# Get how to order the events
	order_by = ''
	if   'sort'		in request.GET: order_by = request.GET['sort']
	elif 'sort_by' 	in request.GET: order_by = request.GET['sort_by']
	elif 'order' 	in request.GET: order_by = request.GET['order']
	elif 'order_by' in request.GET: order_by = request.GET['order_by']
	
	# If days is set, get all events back this number of days
	if 'days' in request.GET:
		events = Event.get_events(days=request.GET['days'], order_by=order_by)
	
	# If events is set, get this number of events
	elif 'events' in request.GET:
		events = Event.get_events(events=request.GET['events'], order_by=order_by)
	
	# If start and end are set (YYYY-MM-DD), get all events between (inclusive)
	elif 'start' in request.GET and 'end' in request.GET:
		events = Event.get_events(events=request.GET['events'], order_by=order_by)
	
	# If start timestamp (YYYY-MM-DD) is set, get all events from this date
	elif 'start' in request.GET:
		events = Event.get_events(start=request.GET['start'], order_by=order_by)
	
	# If end timestamp (YYYY-MM-DD) is set, get all events up to and including this event
	elif 'end' in request.GET:
		events = Event.get_events(end=request.GET['end'], order_by=order_by)
	
	# If surfice is set, get all events associated with this surfice
	elif 'surfice' in request.GET:
		events = Event.get_events(surfice=request.GET['surfice'], order_by=order_by)
	
	# If status is set, get all events that have a certain status
	elif 'status' in request.GET:
		events = Event.get_events(status=request.GET['status'], order_by=order_by)
	
	# If nothing is set, get all events
	else:
		events = Event.get_events(order_by=order_by)
	
	# Serialize the events so that we can pass them back as JSON
	events = EventSerializer(events)
	events = JSONRenderer().render(events.data)
	
	return events

@permission_required('is_superuser', raise_exception=True)
def get_ding(request):
	""" Get a ding
		
		This will either get ding by id
		or get the first/last ding of a page
		based on pagination settings in views.py

		INPUT
		request				A request object
			- ding			The pk of the ding
			- page			The pagination page of the ding
			- first, last	Get the first or last ding on the page
		
		RETURNS
		Ding
	"""
	
	ding = {}
	
	# The ding pk needs to be in request
	if 'ding' in request.GET:
		# Get the ding object from the database
		ding = Ding.get_ding(pk=request.GET['ding'])
		
		# Serialize the ding
		ding = DingSerializer(ding)
		
		# Get the actual data and put it in ding
		ding = ding.data
		
		# Get the ding's surfice, status, and ding urls
		ding['surfice']['url'] = reverse('surfices') + '#surfice-' + slugify(ding['surfice']['name'])
		ding['status']['url'] = reverse('statuses') + '#status-' + slugify(ding['status']['name'])
		ding['url'] = reverse('ding', kwargs={'ding': ding['id']})
		
		# Render the ding out as JSON
		ding = JSONRenderer().render(ding)
	
	elif 'page' in request.GET:
		# For ease of use, get the page
		page = request.GET['page']
	
		# Initialize paginator
		# 10 per page references what is views.py
		dings = Ding.get_dings()
		paginator = Paginator(dings, 10)
	
		# Fill the dings array with the current page
		try:
			dings_page = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver the first page
			dings_page = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver the last page of dings
			dings_page = paginator.page(paginator.num_pages)
		
		if 'first' in request.GET:
			ding = dings[0]
		elif 'last' in request.GET:
			ding = dings[dings_page.end_index()-1]
		
		# Serialize the ding object
		ding = DingSerializer(ding)
		
		# Get the actual data and put it in ding
		ding = ding.data
		
		# Get the ding's surfice, status, and ding urls
		ding['surfice']['url'] = reverse('surfices') + '#surfice-' + slugify(ding['surfice']['name'])
		ding['status']['url'] = reverse('statuses') + '#status-' + slugify(ding['status']['name'])
		ding['url'] = reverse('ding', kwargs={'ding': ding['id']})
		
		# Render the ding out to JSON
		ding = JSONRenderer().render(ding)
	
	# If ding or page were not in the request, throw an error
	else:
		ding.append("A ding or page was not passed")
	
	return ding

@permission_required('is_superuser', raise_exception=True)
def get_dings(request):
	""" Get an array of dings
		
		Only one order_by and one get mode can be used at a time.
		For example, I can order by timestamp, over a certain number of days
		
		INPUT
		request			A request object
			- email				The email address of the person who submitted the ding
			- days				int in number of days back from the current day to pull dings
			- dings				int number of dings to pull regardless of date
			- start				timestamp (YYYY-MM-DD) of the start date of dings
			- end				timestamp (YYYY-MM-DD) of the end date. Gets dings
			-					from before and including this date
			- start, end		if both are set, all dings between (inclusive)
			-					will be returned
			- surfice			Dings related to this surfice
			- status			The reported status stored in the ding
			- [sort, sort_by,
			- order, order_by] 	Allows custom sorting, and then sorting by
			-					timestamp and then pk
			- [none]			If no argument is passed, all stored dings will be returned
			-
			- RETURNS
			- Array of dings in reverse chronological order (newest first)
		
		RETURNS
		*Ding in order_by order or reverse chronological order (newest first)
	"""
	
	dings = {}
	
	# Get how to order the dings
	order_by = ''
	if   'sort'		in request.GET: order_by = request.GET['sort']
	elif 'sort_by' 	in request.GET: order_by = request.GET['sort_by']
	elif 'order' 	in request.GET: order_by = request.GET['order']
	elif 'order_by' in request.GET: order_by = request.GET['order_by']
	
	# If email is set, get all dings associated with this email address
	if 'email' in request.GET:
		dings = Ding.get_dings(email=request.GET['email'], order_by=order_by)
	
	# If days is set, get all dings back this number of days
	elif 'days' in request.GET:
		dings = Ding.get_dings(days=request.GET['days'], order_by=order_by)
	
	# If dings is set, get this number of dings
	elif 'dings' in request.GET:
		dings = Ding.get_dings(dings=request.GET['dings'], order_by=order_by)
	
	# If start and end are set (YYYY-MM-DD), get all dings between (inclusive)
	elif 'start' in request.GET and 'end' in request.GET:
		dings = Ding.get_dings(dings=request.GET['dings'], order_by=order_by)
	
	# If start timestamp (YYYY-MM-DD) is set, get all dings from this date
	elif 'start' in request.GET:
		dings = Ding.get_dings(start=request.GET['start'], order_by=order_by)
	
	# If end timestamp (YYYY-MM-DD) is set, get all dings up to and including this ding
	elif 'end' in request.GET:
		dings = Ding.get_dings(end=request.GET['end'], order_by=order_by)
	
	# If surfice is set, get all dings associated with this surfice
	elif 'surfice' in request.GET:
		dings = Ding.get_dings(surfice=request.GET['surfice'], order_by=order_by)
	
	# If status is set, get all dings that have a certain status
	elif 'status' in request.GET:
		dings = Ding.get_dings(status=request.GET['status'], order_by=order_by)
	
	# If nothing is set, get all dings
	else:
		dings = Ding.get_dings(order_by=order_by)
	
	# Serialize the dings so that we can pass them back as JSON
	dings = DingSerializer(dings)
	dings = JSONRenderer().render(dings.data)
	
	return dings

def get_surfice_dings_length(request):
	""" Get the number of dings returned for a specific surfice
		
		Only one order_by and one get mode can be used at a time.
		For example, I can order by timestamp, over a certain number of days
		
		INPUT
		request			A request object
			- email				The email address of the person who submitted the ding
			- days				int in number of days back from the current day to pull dings
			- dings				int number of dings to pull regardless of date
			- start				timestamp (YYYY-MM-DD) of the start date of dings
			- end				timestamp (YYYY-MM-DD) of the end date. Gets dings
			-					from before and including this date
			- start, end		if both are set, all dings between (inclusive)
			-					will be returned
			- surfice (required)Dings related to this surfice
			- status			The reported status stored in the ding
			- [none]			If no argument is passed, all stored dings will be returned
			-
			- RETURNS
			- Array of dings in reverse chronological order (newest first)
		
		RETURNS
		*Ding in order_by order or reverse chronological order (newest first)
	"""
	
	dings = {}
	
	# Get how to order the dings
	order_by = ''
	
	# Get the surfice
	if 'surfice' in request.GET:
		surfice = request.GET['surfice']
	else:
		dings.append("No Surfice given!")
		return dings
	
	# If email is set, get all dings associated with this email address
	if 'email' in request.GET:
		dings = Ding.get_dings(email=request.GET['email'], order_by=order_by).filter(surfice=surfice)
	
	# If days is set, get all dings back this number of days
	elif 'days' in request.GET:
		dings = Ding.get_dings(days=int(request.GET['days']), order_by=order_by).filter(surfice=surfice)
	
	# If dings is set, get this number of dings
	elif 'dings' in request.GET:
		dings = Ding.get_dings(dings=request.GET['dings'], order_by=order_by).filter(surfice=surfice)
	
	# If start and end are set (YYYY-MM-DD), get all dings between (inclusive)
	elif 'start' in request.GET and 'end' in request.GET:
		dings = Ding.get_dings(dings=request.GET['dings'], order_by=order_by).filter(surfice=surfice)
	
	# If start timestamp (YYYY-MM-DD) is set, get all dings from this date
	elif 'start' in request.GET:
		dings = Ding.get_dings(start=request.GET['start'], order_by=order_by).filter(surfice=surfice)
	
	# If end timestamp (YYYY-MM-DD) is set, get all dings up to and including this ding
	elif 'end' in request.GET:
		dings = Ding.get_dings(end=request.GET['end'], order_by=order_by).filter(surfice=surfice)
	
	# If status is set, get all dings that have a certain status
	elif 'status' in request.GET:
		dings = Ding.get_dings(status=request.GET['status'], order_by=order_by).filter(surfice=surfice)
	
	# If today is set, get all the dings that have happened on this calendar day
	elif 'today' in request.GET:
		from datetime import date
		dings = Ding.get_dings(start=date.today(), order_by=order_by).filter(surfice=surfice)
	
	# If nothing is set, get all dings
	else:
		dings = Ding.get_dings(order_by=order_by).filter(surfice=surfice)
	
	# Serialize the dings so that we can pass them back as JSON
	#dings = DingSerializer(dings)
	#dings = JSONRenderer().render(dings.data)
	
	data = len(dings)
	data = JSONRenderer().render(data)
	
	return data

def dispatch(request, action=''):
	""" Dispatch all ajax functions
		
		Fires functions based on the action passed.
		If no action is passed, nothing happens
		
		INPUT
		request				A request object
		action				A string that corresponds to a function
		
		ACTIONS
		set-status			Set status of a surfice
		set-surf-status		Set status of an entire surfice
		set-surf			Set surf of a surfice
		set-surfs			Set surfs of a surfice
		add-surf			Add surf to a surfice
		add-surfs			Add surfs to a surfice
		update-surf			Update info of surf
		update-surfice		Update info of surfice
		update-status		Update info of status
		update-event		Update info of event
		delete-surf 		Delete a surf
		delete-surfice 		Delete a surfice
		delete-status		Delete a status
		delete-event		Delete an event
		delete-ding			Delete a ding
		submit-ding			Submit a ding
		send-email			Send an email
		get-surf			Get a surf
		get-surfs			Get array of surfs
		get-surfice			Get a surfice
		get-surfices		Get array of surfices
		get-status			Get a status
		get-statuses		Get array of statuses
		get-event			Get an event
		get-events			Get an array of events
		get-ding			Get a ding
		get-dings			Get an array of dings
		get-surfice-dings-length	Get the length of dings assigned to a surfice
		
		RETURNS
		JSON HttpResponse
	"""
	
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
	
	# Set the surfs of a surfice
	elif action == 'set-surfs':
		response = json.dumps(set_surfs(request))
	
	# Add a surf to a surfice
	elif action == 'add-surf':
		response = json.dumps(add_surf(request))
	
	# Add surfs to a surfice
	elif action == 'add-surfs':
		response = json.dumps(add_surfs(request))
	
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
	
	# Delete a surf
	elif action == 'delete-surf':
		response = json.dumps(delete_surf(request))
	
	# Delete a surfice
	elif action == 'delete-surfice':
		response = json.dumps(delete_surfice(request))
	
	# Delete a status
	elif action == 'delete-status':
		response = json.dumps(delete_status(request))
	
	# Delete an event
	elif action == 'delete-event':
		response = json.dumps(delete_event(request))
	
	# Delete a ding
	elif action == 'delete-ding':
		response = json.dumps(delete_ding(request))
	
	# Submit a ding from the user
	elif action == 'submit-ding':
		response = json.dumps(submit_ding(request))
	
	# Send an email
	elif action == 'send-email':
		response = json.dumps(send_email(request))
	
	# Submit an RT ticket
	elif action == 'submit-rt-ticket':
		response = json.dumps(submit_rt_ticket(request))
	
	# Get a single surf
	elif action == 'get-surf':
		response = get_surf(request)
	
	# Get a set of surfs
	elif action == 'get-surfs':
		response = get_surfs(request)
	
	# Get a single surfice
	elif action == 'get-surfice':
		response = get_surfice(request)
	
	# Get a set of surfices
	elif action == 'get-surfices':
		response = get_surfices(request)
	
	# Get a single status
	elif action == 'get-status':
		response = get_status(request)
	
	# Get all statuses
	elif action == 'get-statuses':
		response = get_statuses(request)
	
	# Get a single event
	elif action == 'get-event':
		response = get_event(request)
	
	# Get a set of events
	elif action == 'get-events':
		response = get_events(request)
	
	# Get a single ding
	elif action == 'get-ding':
		response = get_ding(request)
	
	# Get a set of dings
	elif action == 'get-dings':
		response = get_dings(request)
	
	# Get number of dings for the user on the frontend
	elif action == 'get-surfice-dings-length':
		response = get_surfice_dings_length(request)
	
	else:
		response = ["No action called " + action]
	
	return HttpResponse(response, content_type='application/json')
