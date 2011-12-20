from django.conf.urls.defaults import *
#from django.conf.urls import patterns, url, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^accounts/login/$', 'django.contrib.auth.views.login'),
	(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
	# Uncomment the admin/doc line below to enable admin documentation:
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
	
	#(r'^test/', include('default.views.index')),#include('cloudport.index')),
	#(r'^$', 'direct_to_template', {'template': 'index.html'}),
	(r'^time/','cloudport.polls.views.time'),
	(r'^manager/', include('cloudport.job_manager.urls')),
	#(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/cloudport/static', 'show_indexes':True}),
	#(r'^static/(?P<path>.*)$', 'django.contrib.staticfiles.views'), #probably doesn't do anything
	#(r'^jobs_finished/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/jobs_dispatcher/jobs_finished/', 'show_indexes':True}),
	(r'^rest/', include('cloudport.rest.urls')),
	
	(r'^', 'cloudport.default.views.index'),
)
