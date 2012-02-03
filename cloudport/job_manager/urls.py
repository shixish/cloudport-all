from django.conf.urls.defaults import *
#from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    #(r'^$', 'direct_to_template', {'template': 'index.html'}),
    (r'^test', 'cloudport.job_manager.views.req_data'),
    (r'^files', 'cloudport.job_manager.views.get_user_files'),
    #(r'^test', 'cloudport.job_manager.views.testing'),
    #(r'^get/(.*)', 'cloudport.job_manager.views.get'),
    (r'^success/(.*)', 'cloudport.job_manager.views.success'),
    (r'^new/job', 'cloudport.job_manager.views.new_job'),
    (r'^new/file', 'cloudport.job_manager.views.new_file'),
    (r'^', 'cloudport.job_manager.views.manager'),
)