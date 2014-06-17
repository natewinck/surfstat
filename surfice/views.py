from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

#Test with Django tango
def index(request):
	return HttpResponse("Rango says hello world!")