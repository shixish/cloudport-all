from django.conf.urls.defaults import *
#from django.conf.urls import patterns, url, include
from cloudport import settings
from django.conf.urls.static import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#from filebrowser.sites import site

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#tastypie
from cloudport.api import JobResource, UserResource
from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(JobResource())

urlpatterns = patterns('',
    (r'^grappelli/', include('grappelli.urls')),
    #url(r'^admin/filebrowser/', include(site.urls)),
    
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    
    #(r'^test/', include('default.views.index')),#include('cloudport.index')),
    #(r'^$', 'direct_to_template', {'template': 'index.html'}),
    #(r'^time/','cloudport.polls.views.time'),
    (r'^manager/', include('cloudport.job_manager.urls')),
    (r'^media/get/(?P<path>.*)', 'cloudport.job_manager.views.download'),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/cloudport/static', 'show_indexes':True}),
    #(r'^static/(?P<path>.*)$', 'django.contrib.staticfiles.views'), #probably doesn't do anything
    #(r'^jobs_finished/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/jobs_dispatcher/jobs_finished/', 'show_indexes':True}),
    (r'^rest/', include('cloudport.rest.urls')),
    (r'^api/', include(v1_api.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    
    
    #(r'^favicon.ico', HttpResponseRedirect('/manager/success/')),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),
    url("", include("django_socketio.urls")),
    (r'^$', 'cloudport.views.index'),
    #(r'^', 'cloudport.default.views.index'),
)