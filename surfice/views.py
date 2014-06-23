#import logging
from django.shortcuts import render
from django.http import HttpResponse
#from django.template import Context, Template
from surfice.models import Surf, Surfice, Status, Ding, Event

# Create your views here.

# Test with Django tango
def index(request):
	
	# Query the database for a list of ALL surfices currently stored.
	# Order them by status in descending order
	# Retrieve the top 5 only (the "-" in front of it) - or all if less than 5
	# Place the list in our context_dict dictionary which
	# will be passed to the template engine
	#surfice_list = Surfice.objects.order_by('-status')[:5]
	#context_dict = {'surfices': surfice_list}
	
	# Query for surfs = add the list to our context dictionary.
	surf_list = Surf.objects.order_by('-name')[:5]
	context_dict = {'surfs': surf_list}
	
	# We loop through each category returned, and create a URL attribute.
	# This attribute stores an encoded URL
	for surf in surf_list:
		surf.url = surf.name.replace(' ', '_')
	
	# The context is already figured out by the render() shortcut so...
	# Render the response and send it back!
	return render(request, 'surfice/index.html', context_dict)
	
	#return HttpResponse("Rango says hello world!")


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
	
	surfices = Surf.get_surfices(surf_name=surf_name)
	
	if surfices:
		# Add our results list to the template context under name 'surfices'.
		context_dict['surfices'] = surfices
		
		# Also add the surf object from the database to the context dictionary
		# We'll use this in the template to verify the category exists.
		context_dict['surf'] = Surf.objects.get(name=surf_name)
	print Event.get_events(end='2014-06-19')	
	# Go render the response and return it to the client
	return render(request, 'surfice/surf.html', context_dict)
