from django.shortcuts import render
from django.http import HttpResponse
# This is the request handler for the playground app. It defines a view function that returns a simple HTTP response with the text "Hello World". This view can be accessed via the URL pattern defined in the playground/urls.py file.
# Create your views here.
#view function for playground app
def say_hello(request):
    x = 10
    y = 20
    z = x + y
    return HttpResponse('Hello World')