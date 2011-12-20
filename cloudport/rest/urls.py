from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect #for redirecting the browser

#To do with the RESTful API:
from djangorestframework.resources import ModelResource
from djangorestframework.views import ListOrCreateModelView, InstanceModelView, ListModelView
from cloudport.job_manager.models import Job
from cloudport.job_manager.models import DataFile
from djangorestframework import permissions, authentication

class Jobs(ModelResource):
    model = Job
    
class DataFiles(ModelResource):
    model = DataFile

urlpatterns = patterns('',
    url(r'^job/$', ListOrCreateModelView.as_view(resource=Jobs, permissions=(permissions.IsAuthenticated,))),
    url(r'^job/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=Jobs, permissions=(permissions.IsAuthenticated,))),
    url(r'^files/$', ListOrCreateModelView.as_view(resource=DataFiles, permissions=(permissions.IsAuthenticated,))),    
    url(r'^files/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=DataFiles, permissions=(permissions.IsAuthenticated,))),
)