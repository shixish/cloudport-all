from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
#from django.conf.urls import patterns, include, url

def index(request):
    return render_to_response('index.html')