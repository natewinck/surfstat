DEBUG = False

#import logging
from django.shortcuts import render
from django.http import HttpResponse
#from django.template import Context, Template
from surfice.models import Surf, Surfice, Status, Ding, Event
import json

# Create your views here.

def printv(obj, title=""): # Print your variables!
	if title != "":
		print ("\n" + title + "\n"
		   		 "==============================")
	print ''.join("%s: %s\n" % item for item in vars(obj).items())
	
def debug():
	#print Event.get_events(end='2014-06-19')
	
	# Clear database of debug data first
	try: Surf.get_surf('Manual Surf').delete()
	except: pass
	try: Surf.get_surf('Auto Surf').delete()
	except: pass
	try: Surf.get_surf('Auto Surf Without Description').delete()
	except: pass
	try: Status.get_status('Status Without Description').delete()
	except: pass
	try: Status.get_status('Status With Description').delete()
	except: pass
	try: Status.get_status('Status2').delete()
	except: pass
	try: Surfice.get_surfice('Manual Surfice').deleteice()
	except: pass
	try: Surfice.get_surfice('Surfice').deleteice()
	except: pass
	try: Surfice.get_surfice('Surfice1').deleteice()
	except: pass
	try: Surfice.get_surfice('Surfice2').deleteice()
	except: pass
	
	
	# First test Surfs
	# First manually
	surf_manual = Surf()
 	surf_manual.name = "Manual Surf"
 	surf_manual.description = "A description of the manual surf"
 	surf_manual.save_new()
	
	printv(surf_manual, "MANUAL SURF")
	
	# Now automatic Surf
	surf_auto_nodescr = Surf.create("Auto Surf Without Description")
	surf_auto = Surf.create("Auto Surf", "A Description for the Auto")
	printv(surf_auto_nodescr, "AUTO SURF W/O DESCRIPTION")
	printv(surf_auto, "AUTO SURF")
	
	# Now try to overwrite a Surf (it shouldn't work)
	surf_overwrite = Surf.create("Auto Surf")
	print "The following overwrite should not work:"
	try: printv(surf_overwrite, "SURF OVERWRITE")
	except: pass
	
	# Get a Surf by name
	surf_by_name = Surf.get_surf("Auto Surf")
	printv(surf_by_name, "GET AUTO SURF BY NAME")
	
	# Now delete the manual Surf
	surf_manual.delete()
	print "MANUAL SURF STILL SAVED AFTER DELETION? (Should be False)\n============================"
	print Surf.is_saved(surf_manual.name) # Test to see if it worked
	
	
	print "\n\n\n\n"
	
	
	# Second, create a new Status
	status_nodescr = Status.create("Status Without Description", color="#678434")
	status = Status.create("Status With Description", "A description", misc="haha")
	
	printv(status_nodescr, "STATUS W/O DESCRIPTION")
	printv(status, "STATUS WITH DESCRIPTION")
	print(status.data, "DATA of STATUS")
	
	# Get a status by name
	status_by_name = Status.get_status("Status Without Description")
	
	printv(status_by_name, "GET STATUS W/O DESCRIPTION BY NAME")
	
	# Delete the status without a description
	status_by_name.delete()
	
	print "NO DESCRIPTION STILL SAVED? (should be False)\n======================="
	print Status.is_saved("Status Without Description")
	
	status2 = Status.create("Status2", "A 2nd description", possible=5)






	# Now test Surfices
	# First manually
	surfice_manual = Surfice()
	surfice_manual.name = "Manual Surfice"
	surfice_manual.surf = surf_auto
	surfice_manual.description = "Manual Description"
	surfice_manual.status = status # I'm afraid this won't work at all
	surfice_manual.save_new()
	
	printv(surfice_manual, "MANUAL SURFICE")
	
	# Now Delete the manual one
	surfice_manual.delete()
	
	print "Is the Manual Surfice still saved (It should be False)\n========================"
	print Surfice.is_saved(surfice_manual.name)
	
	
	# Now Automatically
	surfice = Surfice.create("Surfice", surf_auto, status, "A Surfice description")
	surfice2 = Surfice.create("Surfice2", surf_auto, status, "A 2nd Surfice description")
	printv(surfice, "SURFICE")
	printv(surfice2, "SURFICE2")
	
	# Try to overwrite it
	surfice_overwrite = Surfice.create("Surfice", surf_auto, status)
	print surfice_overwrite
	
	# Get surfices
	print Surfice.get_surfices(surf=surf_auto) # All the surfices under surf_auto
	print Surfice.get_surfices(name="Surf") # All that contain "Surf"
	print Surfice.get_surfices() # All surfices
	
	
	surfice.set_surf(surf_auto_nodescr)
	surfice.set_description("I have a description now!")
	surfice.set_name("Surfice1")
	surfice.set_status(status2) # Just changes the status without making an event
	surfice.set_status(status, "What happened now?")
	surfice.set_status(status2, "Okay now we're back at status2")
	printv(surfice, "SURFICE1 UPDATED")
	
	
	
	# Delete everything
	try: surf_auto.delete()
	except: pass
	try: surf_auto_nodescr.delete()
	except: pass
	
	try: status_nodescr.delete()
	except: pass
	
	try: status.delete()
	except: pass
	try: status2.delete()
	except: pass
	
	try: surfice.delete()
	except: pass
	try: surfice2.delete()
	except: pass


def ding(request):
	#Not checking yet because this is a test
	#if 'q' in request.POST:
    #    message = 'You searched for: %r' % request.POST['q']
    print(printv(request.POST))
    d = request.POST
    return HttpResponse(d['email'])
    #return render(request, 'surfice/index.html', {})
	#Ding.create(d['surfice'], d['status'], d['email'], d['description'])
	#index(request)

# Test with Django tango
def index(request):
	if DEBUG: debug()
	
	if request.method == 'POST':
		d = request.POST
		if d.get('email') and '@' not in d['email']:
			pass
		else:
			print "AH"
			print Surfice.get_surfice(pk=d['surfice'])
			print Status.get_status(pk=d['status'])
			print d['email']
			print d['description']
			ding = Ding.create(
				Surfice.get_surfice(pk=d['surfice']),
				Status.get_status(pk=d['status']),
				d['email'],
				d['description']
			)
			print ding
	
	# Query the database for a list of ALL surfices currently stored.
	# Order them by status in descending order
	# Retrieve the top 5 only (the "-" in front of it) - or all if less than 5
	# Place the list in our context_dict dictionary which
	# will be passed to the template engine
	#surfice_list = Surfice.objects.order_by('-status')[:5]
	#context_dict = {'surfices': surfice_list}
	
	# Query the database for a list of ALL surfices currently stored.
	surfice_list = Surfice.get_surfices()
	
	# Place the list in our context_dict dictionary which
	# will be passed to the template engine
	context_dict = {'surfices': surfice_list}
	
	# Query the database for a list of all the events
	# Place them in context_dict
	event_list = Event.get_events()
	context_dict['events'] = event_list
	
	
	# Get a list of available statuses for reporting dings
	# Place them in context_dict
	status_list = Status.get_statuses()
	context_dict['statuses'] = status_list
	
	
	
	
	# GET ISSUE STATUS COLOR HERE -------------------------------------
	# SET A DEFAULT STATUS AS AN ISSUE ----------------------------------
	
	
	
	
	
	
	# Query for surfs = add the list to our context dictionary.
	#surf_list = Surf.objects.order_by('-name')[:5]
	#context_dict = {'surfs': surf_list}
	
	# We loop through each category returned, and create a URL attribute.
	# This attribute stores an encoded URL
	#for surf in surf_list:
	#	surf.url = surf.name.replace(' ', '_')
	
	# The context is already figured out by the render() shortcut so...
	# Render the response and send it back!
	return render(request, 'surfice/base_index.html', context_dict)
	
	#return HttpResponse("Rango says hello world!")


def admin(request):
	context_dict = {}
	
	# Query for surfs and add them to context_dict
	surf_list = Surf.get_surfs()
	context_dict['surfs'] = surf_list
	
	# Query for Surfices and add them to context_dict
	surfice_list = Surfice.get_surfices()
	context_dict['surfices'] = surfice_list
	
	# Query for Events and add them to context_dict
	event_list = Event.get_events()
	context_dict['events'] = event_list
	
	# Query for Statuses and add them to context_dict
	status_list = Status.get_statuses()
	context_dict['statuses'] = status_list
	
	return render(request, 'surfice/base_admin.html', context_dict)


def surf(request, surf_url):
	# Change underscores in the category name to spaces.
	# URLs don't handle spaces well, so we encode them as underscores.
	# We can then simply replace the underscores with spaces again to get the name.
	surf_name = surf_url.replace('_', ' ')
	
	# Change spaces to underscores for the url.
	# URLs don't handle spaces well.
	# So we just replace them!
	#url = name.replace(' ', '_')
	
	# Create a context dictionary which we can pass to the template rendering engine
	# We start by containing the name of the surf passed by the user
	context_dict = {'surf_name': surf_name}
	
	surfices = Surf.get_surf(surf_name).get_surfices()
	
	if surfices:
		# Add our results list to the template context under name 'surfices'.
		context_dict['surfices'] = surfices
		
		# Also add the surf object from the database to the context dictionary
		# We'll use this in the template to verify the category exists.
		context_dict['surf'] = Surf.objects.get(name=surf_name)
		
	# Go render the response and return it to the client
	return render(request, 'surfice/surf.html', context_dict)


def surfs(request):
	context_dict = {}
	
	# If the admin is trying to create or delete a Surf, the page is refreshed
	flag = False
	if request.method == 'POST':
			
		# Is the admin trying to delete a status?
		if	(
				'delete' in request.POST and
				'surf' in request.POST and
				'new_surf' in request.POST
			):
			
			# Get the surf that we're about to delete
			surf = Surf.get_surf(pk=request.POST['surf'])
			
			# Get the new surf that we're changing surfices to
			new_surf = Surf.get_surf(pk=request.POST['new_surf'])
			
			# Only continue if the new surf actually exists and is not the same
			# as the one that's being deleted
			if type(new_surf) is Surf and new_surf != surf:
				
				# Get all the surfices associated with this surf
				surfices = surf.get_surfices()
				
				# Now loop through all the surfices and change their surf
				# to the new surf
				for surfice in surfices:
					surfice.set_surf(surf=new_surf)
				
				# Go ahead and delete the surf now that everything has be re-assigned
				surf.delete()
			
			# A new surf wasn't selected or it doesn't exist, so don't do anything
			else:
				pass
		
		# Is the admin trying to create a surf?
		elif 'surf' in request.POST and 'description' in request.POST:
			surf = Surf.create(request.POST['surf'], request.POST['description'])
			if surf == None:
				flag = True
			
	
	
	# Query for surfs and add them to context_dict
	surf_list = Surf.get_surfs()
	context_dict['surfs'] = surf_list
	
	# For each Surf, query for Surfices and add them to context_dict
	for i, surf in enumerate(context_dict['surfs']):
		context_dict['surfs'][i].surfices = surf.get_surfices()
	
	# Query all the Surfices and add them to context_dict
	surfice_list = Surfice.get_surfices()
	context_dict['surfices'] = surfice_list
	
	# Query all the Statuses and add them to context_dict
	status_list = Status.get_statuses()
	context_dict['statuses'] = status_list
	
	
	
	return render(request, 'surfice/base_surfs.html', context_dict)


def surfices(request):
	context_dict = {}
	
	# If the admin is trying to create or delete a Surfice, the page is refreshed
	flag = False
	if request.method == 'POST':
		
		# Is the admin trying to delete a surfice?
		if	(
				'delete' in request.POST and
				'surfice' in request.POST
			):
			
			# Get the surfice that we're about to delete
			surfice = Surfice.get_surfice(pk=request.POST['surfice'])
			
			# Django automatically deletes all related objects
			# along with the surfice so go ahead and delete the surfice
			if type(surfice) is Surfice:
				surfice.delete()
			
			# The code below is equivalent to what the single delete()
			# function above is doing. Django automatically deletes all related
			# objects from the database. Below is just what it does explicitly
				
			## Get all the events and dings associated with this surf
			#events = Event.get_events(surfice=surfice)
			#dings = Ding.get_dings(surfice=surfice)
			
			## Now loop through all these events and delete them
			#for event in events:
			#	event.delete()
			
			## And loop through all these dings and delete them
			#for ding in dings:
			#	ding.delete()
			
			## Go ahead and delete the surfice now that everything associated with it has
			## been deleted
			#surfice.delete()
		
		# Is the admin trying to create a surf?
		elif	(
					'surfice' in request.POST and
					'surf' in request.POST and
					'status' in request.POST
				):
			
			surf = Surf.get_surf(pk=request.POST['surf'])
			status = Status.get_status(pk=request.POST['status'])
			surfice = Surfice.create(request.POST['surfice'], surf, status, request.POST.get('description', ''))
			if surfice == None:
				flag = True
			
	
	
	# Query for surfs and add them to context_dict
	surf_list = Surf.get_surfs()
	context_dict['surfs'] = surf_list
	
	# Query all the Surfices and add them to context_dict
	surfice_list = Surfice.get_surfices()
	context_dict['surfices'] = surfice_list
	
	# Query all the Statuses and add them to context_dict
	status_list = Status.get_statuses()
	context_dict['statuses'] = status_list
	
	
	return render(request, 'surfice/base_surfices.html', context_dict)


def settings(request):
	context_dict = {}
	
	return render(request, 'surfice/base_settings.html', context_dict)

def status(request):
	context_dict = {}
	
	# If the admin is trying to create or delete a Status, the page is refreshed
	flag = False
	if request.method == 'POST':
		# Is the admin trying to delete a status?
		if	(
				'delete' in request.POST and
				'status' in request.POST and
				'new_status' in request.POST
			):
			
			# Get the status that we're about to delete
			status = Status.get_status(pk=request.POST['status'])
			
			# Get the new status that we're changing surfices to
			new_status = Status.get_status(pk=request.POST['new_status'])
			
			# Only continue if the new status actually exists and is not the same
			# as the one that's being deleted
			if type(new_status) is Status and new_status != status:
				
				# Get all the surfices associated with this status
				surfices = Surfice.get_surfices(status=status)
				
				# Now loop through all the surfices and change their status
				# to the status passed through POST
				for surfice in surfices:
					surfice.set_status(status=new_status)
				
				# Go ahead and delete the status now that everything has be re-assigned
				status.delete()
			
			# A new status wasn't selected or it doesn't exist, so don't do anything
			else:
				pass
				
		
		# Is the admin trying to create a status?
		elif 'name' in request.POST:
			
			data = {}
			if 'data' in request.POST:
				# Get the JSON data from POST
				print request.POST['data']
				data = json.loads(request.POST['data'])
				print data
			
			# Set the general data by passing in data as keyword arguments
			status = Status.create	(
										name = request.POST['name'],
										description = request.POST.get('description', ''),
										**data
									)
			if status == None:
				flag = True
	
	# Query all the Statuses and add them to context_dict
	status_list = Status.get_statuses()
	context_dict['statuses'] = status_list
	
	return render(request, 'surfice/base_status.html', context_dict)