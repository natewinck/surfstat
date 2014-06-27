DEBUG = False

#import logging
from django.shortcuts import render
from django.http import HttpResponse
#from django.template import Context, Template
from surfice.models import Surf, Surfice, Status, Ding, Event

# Create your views here.

def printv(obj, title=""): # Print your variables!
	if title != "":
		print ("\n" + title + "\n"
		   		 "==============================")
	print ''.join("%s: %s\n" % item for item in vars(obj).items())
	
def debug():
	#print Event.get_events(end='2014-06-19')
	
	# Clear database of debug data first
	try: Surf.get_surf('Manual Surf').delete_surf()
	except: pass
	try: Surf.get_surf('Auto Surf').delete_surf()
	except: pass
	try: Surf.get_surf('Auto Surf Without Description').delete_surf()
	except: pass
	try: Status.get_status('Status Without Description').delete_status()
	except: pass
	try: Status.get_status('Status With Description').delete_status()
	except: pass
	try: Status.get_status('Status2').delete_status()
	except: pass
	try: Surfice.get_surfice('Manual Surfice').delete_surfice()
	except: pass
	try: Surfice.get_surfice('Surfice').delete_surfice()
	except: pass
	try: Surfice.get_surfice('Surfice1').delete_surfice()
	except: pass
	try: Surfice.get_surfice('Surfice2').delete_surfice()
	except: pass
	
	
	# First test Surfs
	# First manually
	surf_manual = Surf()
 	surf_manual.name = "Manual Surf"
 	surf_manual.description = "A description of the manual surf"
 	surf_manual.save_surf()
	
	printv(surf_manual, "MANUAL SURF")
	
	# Now automatic Surf
	surf_auto_nodescr = Surf.create_surf("Auto Surf Without Description")
	surf_auto = Surf.create_surf("Auto Surf", "A Description for the Auto")
	printv(surf_auto_nodescr, "AUTO SURF W/O DESCRIPTION")
	printv(surf_auto, "AUTO SURF")
	
	# Now try to overwrite a Surf (it shouldn't work)
	surf_overwrite = Surf.create_surf("Auto Surf")
	print "The following overwrite should not work:"
	try: printv(surf_overwrite, "SURF OVERWRITE")
	except: pass
	
	# Get a Surf by name
	surf_by_name = Surf.get_surf("Auto Surf")
	printv(surf_by_name, "GET AUTO SURF BY NAME")
	
	# Now delete the manual Surf
	surf_manual.delete_surf()
	print "MANUAL SURF STILL SAVED AFTER DELETION? (Should be False)\n============================"
	print Surf.is_saved(surf_manual.name) # Test to see if it worked
	
	
	print "\n\n\n\n"
	
	
	# Second, create a new Status
	status_nodescr = Status.create_status("Status Without Description")
	status = Status.create_status("Status With Description", "A description")
	
	printv(status_nodescr, "STATUS W/O DESCRIPTION")
	printv(status, "STATUS WITH DESCRIPTION")
	
	# Get a status by name
	status_by_name = Status.get_status("Status Without Description")
	
	printv(status_by_name, "GET STATUS W/O DESCRIPTION BY NAME")
	
	# Delete the status without a description
	status_by_name.delete_status()
	
	print "NO DESCRIPTION STILL SAVED? (should be False)\n======================="
	print Status.is_saved("Status Without Description")
	
	status2 = Status.create_status("Status2", "A 2nd description")






	# Now test Surfices
	# First manually
	surfice_manual = Surfice()
	surfice_manual.name = "Manual Surfice"
	surfice_manual.surf = surf_auto
	surfice_manual.description = "Manual Description"
	surfice_manual.status = status # I'm afraid this won't work at all
	surfice_manual.save_surfice()
	
	printv(surfice_manual, "MANUAL SURFICE")
	
	# Now Delete the manual one
	surfice_manual.delete_surfice()
	
	print "Is the Manual Surfice still saved (It should be False)\n========================"
	print Surfice.is_saved(surfice_manual.name)
	
	
	# Now Automatically
	surfice = Surfice.create_surfice("Surfice", surf_auto, status, "A Surfice description")
	surfice2 = Surfice.create_surfice("Surfice2", surf_auto, status, "A 2nd Surfice description")
	printv(surfice, "SURFICE")
	printv(surfice2, "SURFICE2")
	
	# Try to overwrite it
	surfice_overwrite = Surfice.create_surfice("Surfice", surf_auto, status)
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
	
	
# 	
	# Delete everything
	try: surf_auto.delete_surf()
	except: pass
	try: surf_auto_nodescr.delete_surf()
	except: pass
	
	try: status_nodescr = delete_status()
	except: pass
	
	try: status.delete_status()
	except: pass
	try: status2.delete_status()
	except: pass
	
	try: surfice.delete_surfice()
	except: pass
	try: surfice2.delete_surfice()
	except: pass


def ding(request):
	#Not checking yet because this is a test
	#if 'q' in request.POST:
    #    message = 'You searched for: %r' % request.POST['q']
    print(printv(request.POST))
    d = request.POST
    return HttpResponse(d['email'])
    #return render(request, 'surfice/index.html', {})
	#Ding.create_ding(d['surfice'], d['status'], d['email'], d['description'])
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
			print Surfice.get_surfice(id=d['surfice'])
			print Status.get_status(id=d['status'])
			print d['email']
			print d['description']
			ding = Ding.create_ding(
				Surfice.get_surfice(id=d['surfice']),
				Status.get_status(id=d['status']),
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
	return render(request, 'surfice/index.html', context_dict)
	
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
	
	return render(request, 'surfice/admin.html', context_dict)


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
	return render(request, 'surfice/surfs.html')
def surfices(request):
	return render(request, 'surfice/surfices.html')
def settings(request):
	return render(request, 'surfice/settings.html')
def status(request):
	return render(request, 'surfice/status.html')