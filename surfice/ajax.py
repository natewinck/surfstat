from surfice.models import Surf, Surfice, Status, Ding, Event
from django.http import HttpResponse

def ajax(request, action=''):
	print "hello?"
	
	if action == 'set-status':
		# If neither surfice nor status are present,
		# don't do anything
		if not request.POST.get('surfice'):
			print "no surfice"
			pass
		
		elif not request.POST.get('status'):
			# Do nothing
			print "no status"
			pass
		else:
			print "ELSE"
			# Get the surfice and status parameters to set the status of the surfice
			surfice = Surfice.get_surfice(id=request.POST['surfice'])
			status = Status.get_status(id=request.POST['status'])
			
			# Get the description. If no description was passed,
			# fill it in with the default value of the empty string
			# Using .get() allows for description not being set in POST
			description = request.POST.get('description','')
			
			surfice.set_status(status, description)
		
	elif action == 'set-surf-status':
		# If neither surfice nor status are present,
		# don't do anything
		if not request.POST.get('surf') or not request.POST.get('status'):
			# Do nothing
			print "oops"
			pass
		else:
			# Get the surf and status parameters to set the status of the surfice
			surf = Surf.get_surf(id=request.POST['surf'])
			status = Status.get_status(id=request.POST['status'])
			print surf
			# Get the description. If no description was passed,
			# fill it in with the default value of the empty string
			# Using .get() allows for description not being set in POST
			description = request.POST.get('description','')
			
			# Get all the surfices associated with this surf
			surfices = surf.get_surfices()
			
			# Now set the status for all the Surfices in this Surf
			for surfice in surfices:
				surfice.set_status(status, description)
			
			
	return HttpResponse()