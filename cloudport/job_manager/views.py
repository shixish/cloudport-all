# Create your views here.
from django.http import HttpResponse #for direct html output
from django.http import HttpResponseRedirect #for redirecting the browser
from django.core.context_processors import csrf #needed for file upload
from django.shortcuts import render_to_response #implements a template file
from django.template import RequestContext #provides some extra variables to my templates
from django.contrib.auth.decorators import login_required #provides the @login_required() syntax


from cloudport.settings import MEDIA_ROOT
from cloudport.job_manager.forms import * #lets me use the forms i added in the forms file
from cloudport.job_manager.models import * #lets me use models...

import os #for directory listing
import json
from datetime import datetime

from django.core import serializers
def req_data(request):
    #from datetime import date
    #import time
    #job1 = Job(date=date.today(), title="Test 1", status=0)
    #job1.save()
    
    
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
def new_job(request):
    if request.method == 'POST':
        post = request.POST.copy() 
        post['creator'] = request.user.id
        post['editor'] = request.user.id
        
        form = JobForm(post, request.FILES)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect('/manager/success/')#%request.POST['title'])
            return HttpResponse('{"status":"success"}')
        else:
            errors = json.dumps(form.errors);
            return HttpResponse('{"status":"fail", "errors":'+errors+'}')
    #else:
    #    form = JobForm()
    #c = RequestContext(request)
    #c.update(csrf(request))
    #return render_to_response('job_manager/jobform.html', {'form': form}, c)
    return HttpResponse('{"status":"fail", "error":"No data"}')

#'check_password', 'clean', 'clean_fields', 'date_error_message', 'date_joined', 'delete', 'email', 'email_user', 'file_creator', 'file_editor', 'first_name', 'full_clean', 'get_absolute_url', 'get_all_permissions', 'get_and_delete_messages', 'get_full_name', 'get_group_permissions', 'get_next_by_date_joined', 'get_next_by_last_login', 'get_previous_by_date_joined', 'get_previous_by_last_login', 'get_profile', 'groups', 'has_module_perms', 'has_perm', 'has_perms', 'has_usable_password', 'id', 'is_active', 'is_anonymous', 'is_authenticated', 'is_staff', 'is_superuser', 'job_creator', 'job_editor', 'last_login', 'last_name', 'logentry_set', 'message_set', 'objects', 'password', 'pk', 'prepare_database_save', 'save', 'save_base', 'serializable_value', 'set_password', 'set_unusable_password', 'unique_error_message', 'user_permissions', 'username', 'validate_unique']

#from django.forms.util import ErrorList
#@login_required()
#def new_file(request):
#    if request.method == 'POST':
#        post = request.POST.copy() 
#        post['creator'] = request.user.id
#        post['editor'] = request.user.id
#        
#        form = DataFileForm(post, request.FILES)
#        if form.is_valid():
#            form.save()
#            #return HttpResponseRedirect('/manager/success/')#%request.POST['title'])
#            return HttpResponse('{"status":"success"}')
#        else:
#            errors = json.dumps(form.errors);
#            return HttpResponse('{"status":"fail", "errors":'+errors+'}')
#    #else:
#        #form = JobForm()
#    #c = RequestContext(request)
#    #c.update(csrf(request))
#    return HttpResponse('{"status":"fail", "error":"No data"}')
    
@login_required()
def new_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #handle_uploaded_file(request, request.FILES['file'])
            return handle_uploaded_file(request, request.FILES['file'])
            #return HttpResponse('{"status":"success"}')
        else:
            errors = json.dumps(form.errors);
            return HttpResponse('{"status":"fail", "errors":'+errors+'}')
    return HttpResponse('{"status":"fail", "error":"No data"}')    
    #return render_to_response('job_manager/upload.html', {'form': form}, c)

#cant use @login_required because this doesn't take a request variable... could change that.
@login_required()
def handle_uploaded_file(request, f):
    directory = MEDIA_ROOT+'users/'+str(request.user.id)+'/'
    if not os.path.exists(directory):
        os.mkdir(directory)
    
    if os.path.exists(directory):
        destination = open(directory+f.name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        return HttpResponse('{"status":"success"}')
    else:
        return HttpResponse('{"status":"fail", "error":"Unable to upload file. Bad directory."}')


def humanize_bytes(bytes, precision=1):
    abbrevs = (
        (1<<50L, 'PB'),
        (1<<40L, 'TB'),
        (1<<30L, 'GB'),
        (1<<20L, 'MB'),
        (1<<10L, 'kB'),
        (1, 'bytes')
    )
    if bytes == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytes >= factor:
            break
    return '%.*f %s' % (precision, bytes / factor, suffix)

def format_files(directory, path):
    s = os.stat(directory+path)
    return {
        'name':path,
        'modified':datetime.fromtimestamp(s.st_mtime).strftime('%Y-%m-%d %I:%M %p'),
        'mtime':s.st_mtime,
        'size':humanize_bytes(s.st_size)
    }

@login_required()
def get_user_files(request):
    directory = MEDIA_ROOT+'users/'+str(request.user.id)+'/'
    if os.path.exists(directory):
        filelist = os.listdir(directory)
        filelist = filter(lambda x: not os.path.isdir(directory+x), filelist)
        filelist = map(lambda x: format_files(directory, x), filelist)
        #newest = max(filelist, key=lambda x: os.stat(dir+x))
        #return HttpResponse(repr(filelist))
        return HttpResponse(json.dumps(filelist))
    else:
        return HttpResponse('[]')

@login_required()
def manager(request):
    #items = get_job_list()
    #return render_to_response('job_manager/manager.html', {"items":items}, context_instance=RequestContext(request))
    c = RequestContext(request)
    c.update(csrf(request))
    return render_to_response('job_manager/manager.html', {'file_form':UploadFileForm(), 'job_form':JobForm(), 'bootstrap':'TODO'}, c)

