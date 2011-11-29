# Create your views here.
from django.http import HttpResponse #for direct html output
from django.http import HttpResponseRedirect #for redirecting the browser
from django.core.context_processors import csrf #needed for file upload
from django.shortcuts import render_to_response #implements a template file
from django.template import RequestContext #provides some extra variables to my templates
from django.contrib.auth.decorators import login_required #provides the @login_required() syntax
import os #for directory listing

from cloudport.job_manager.forms import * #lets me use the forms i added in the forms file
from cloudport.job_manager.models import * #lets me use models...


from django.core import serializers
def req_data(request):
    #from datetime import date
    #import time
    #job1 = Job(date=date.today(), title="Test 1", status=0)
    #job1.save()
    
    import json
    jobs = Job.objects.all()
    #return HttpResponse(jobs)
    return HttpResponse(serializers.serialize('json', jobs))
    #return HttpResponse(repr(request))

#def testing(request):
#    return render_to_response('test.html', {'bootstrap':"TODO"})

@login_required()
def success(request, title):
    return HttpResponse("The file upload appears to have gone smoothly. <br> <a href=\"/manager/\">go back to manager</a>")

@login_required()
def upload_file(request):
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/manager/success/')#%request.POST['title'])
    else:
        form = JobForm()
    c = RequestContext(request)
    c.update(csrf(request))
    return render_to_response('job_manager/jobform.html', {'form': form}, c)

#def get_job_list():
#    items = [
#        {"id":0, "done": False, "name":"Bob job"},
#        {"id":1, "done": False, "name":"Bill job"},
#        {"id":2, "done": False, "name":"job 345"},
#        {"id":3, "done": True, "name":"Jill job", "output":"infosthetics02.jpg"},
#        {"id":4, "done": True, "name":"Crazy cool job", "output":"graphs.jpg"},
#    ]
#    dir = "/home/jobs_dispatcher/jobs_finished/"
#    filelist = os.listdir(dir)
#    filelist = filter(lambda x: not os.path.isdir(dir+x), filelist)
#    newest = max(filelist, key=lambda x: os.stat(dir+x).st_mtime)
#    items.append({"id":5, "done": True, "name":"Latest Result", "output":newest})
#    return items
#from django.core import serializers
#import json
#@login_required()
#def get(request, thing):
#    if (thing == 'jobs'):
#        #return HttpResponse(serializers.serialize('json', Job.objects.all()))
#        return HttpResponse(json.dumps(get_job_list()))

@login_required()
def manager(request):
    #items = get_job_list()
    #return render_to_response('job_manager/manager.html', {"items":items}, context_instance=RequestContext(request))
    c = RequestContext(request)
    c.update(csrf(request))
    return render_to_response('job_manager/manager.html', {'form':JobForm(), 'bootstrap':"TODO"}, c)

