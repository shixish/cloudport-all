from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect #for redirecting the browser

#To do with the RESTful API:
from djangorestframework.resources import ModelResource
from djangorestframework.views import ListOrCreateModelView, InstanceModelView, ListModelView
from cloudport.job_manager.models import Job
from djangorestframework import permissions, authentication

class MyResource(ModelResource):
    model = Job

urlpatterns = patterns('',
    url(r'^job/$', ListOrCreateModelView.as_view(resource=MyResource, permissions=(permissions.IsAuthenticated,))),
    url(r'^job/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=MyResource, permissions=(permissions.IsAuthenticated,))),
)