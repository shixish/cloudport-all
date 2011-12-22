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
    exclude = ('id', 'pk', 'creator', 'editor')
    include = None
    
class DataFiles(ModelResource):
    model = DataFile
    exclude = ('id', 'pk', 'creator', 'editor')
    include = None
    
    #def get(self, request, auth, *args, **kwargs):
    #    try:
    #        if args:
    #            # If we have any none kwargs then assume the last represents the primrary key
    #            instance = self.model.objects.get(pk=args[-1], **kwargs)
    #        else:
    #            # Otherwise assume the kwargs uniquely identify the model
    #            instance = self.model.objects.get(**kwargs)
    #    except self.model.DoesNotExist:
    #        raise ResponseException(status.HTTP_404_NOT_FOUND)
    #
    #    return instance
    
#class MockView(View):
#            permissions = ()
#            form = FileForm
#            def post(self, request, *args, **kwargs):
#                return {'FILE_NAME': self.CONTENT['file'].name,
#                        'FILE_CONTENT': self.CONTENT['file'].read()}

urlpatterns = patterns('',
    url(r'^job/$', ListOrCreateModelView.as_view(resource=Jobs, permissions=(permissions.IsAuthenticated,))),
    url(r'^job/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=Jobs, permissions=(permissions.IsAuthenticated,))),
    url(r'^files/$', ListOrCreateModelView.as_view(resource=DataFiles, permissions=(permissions.IsAuthenticated,))),    
    url(r'^files/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=DataFiles, permissions=(permissions.IsAuthenticated,))),
)