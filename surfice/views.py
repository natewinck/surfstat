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
	surfice_list = Surfice.objects.order_by('-status')[:5]
	context_dict = {'surfices': surfice_list}
	
	# The context is already figured out by the render() shortcut so...
	# Render the response and send it back!
	return render(request, 'surfice/index.html', context_dict)
	
	#return HttpResponse("Rango says hello world!")