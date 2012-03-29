# Create your views here.
from django.http import HttpResponse #for direct html output
from django.http import HttpResponseRedirect #for redirecting the browser
from django.http import Http404
from django.core.context_processors import csrf #needed for file upload
from django.shortcuts import render_to_response #implements a template file
from django.template import RequestContext #provides some extra variables to my templates
from django.contrib.auth.decorators import login_required #provides the @login_required() syntax

from cloudport.settings import MEDIA_ROOT
from cloudport.settings import TASK_UPLOAD_FILE_EXTENSIONS
from cloudport.job_manager.forms import * #lets me use the forms i added in the forms file
from cloudport.job_manager.models import * #lets me use models...

from django.contrib.auth.decorators import user_passes_test
from django_socketio import events, broadcast, broadcast_channel, NoSocket

import os #for directory listing
import json
import threading
import subprocess
import logging
from datetime import datetime

import cPickle
import random

from django.core import serializers
def req_data(request):
    #from datetime import date
    #import time
    #job1 = Job(date=date.today(), title="Test 1", status=0)
    #job1.save()
    return HttpResponse(str(os.environ['mod_wsgi.version']))
    
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
        #post = request.POST.copy() 
        #post['creator'] = request.user.id
        #post['editor'] = request.user.id
        
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.creator = request.user
            job.editor = request.user
            job.save()
            run(job)
            #t = ThreadClass(job)
            #t.start()
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

#it appears that this is a bad way of doing this, but should work for now.
@login_required()
def download(request, path):
    directory = MEDIA_ROOT+'users/'+str(request.user.id)+'/'
    #in unix you can specify a filename like this "../../home/private"
    #which would end up looking like this /var/www-django/../../home/private
    #this would give you access to files you are not supposed to be able to get to...
    if ('..' not in path and os.path.isfile(directory+path)):
        response = HttpResponse() # 200 OK
        del response['content-type'] # We'll let the web server guess this.
        response['X-Sendfile'] = directory+path
        return response
    raise Http404

def run(job):
    directory = MEDIA_ROOT+'users/'+str(job.editor.id)+'/'
    fn = job.filename
    ext = os.path.splitext(fn)[1][1:]
    job_filename = "/var/www-django/jobsd/jobs_uploads/%s"%random.randint(1,9999999999999)
    logging.debug("Writing file: %s"%job_filename)
    cPickle.dump({"directory":directory, "file":fn, "ext":ext}, open(job_filename, "wb"), 2)
    logging.debug("done.")
    
    ##logging.debug("%s recieved %s" % (self.getName(), directory+fn))
    #if (ext == "py"):
    #    logging.debug("starting process... ")
    #    #r = subprocess.Popen(['python', directory+fn])
    #    r = os.system('python %s'%directory+fn)
    #    logging.debug("done. r=%s"%r)

class ThreadClass(threading.Thread):
    def __init__(self, job):
        self.job = job
        threading.Thread.__init__(self)
        
    def run(self):
        directory = MEDIA_ROOT+'users/'+str(self.job.editor.id)+'/'
        fn = self.job.filename
        ext = os.path.splitext(fn)[1][1:]
        logging.debug("%s recieved %s" % (self.getName(), directory+fn))
        if (ext == "py"):
            logging.debug("starting process... ")
            subprocess.Popen(['python', directory+fn])
            r=os.system('python %s'%directory+fn)
            logging.debug("done. r=%s"%r)
        
        #cmdstr = ['python', self.job]
        #process = subprocess.Popen(['ls'],stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setuid(10033))
        #logging.debug(process)

@login_required()
def manager(request):
    c = RequestContext(request)
    c.update(csrf(request))
    return render_to_response('job_manager/manager.html', {'file_form':UploadFileForm(), 'job_form':JobForm(), 'bootstrap':'TODO'}, c)


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
    ext = os.path.splitext(path)[1][1:]
    exe = True if ext in TASK_UPLOAD_FILE_EXTENSIONS else False
    return {
        'filename':path,
        'modified':datetime.fromtimestamp(s.st_mtime).strftime('%Y-%m-%d %I:%M %p'),
        'mtime':s.st_mtime,
        'size':humanize_bytes(s.st_size),
        'ext':ext,
        'exe':exe
    }

#SOCKET.IO STUFF

#@events.on_message(channel="^room-")
#def message(request, socket, context, message):
#    """
#    Event handler for a room receiving a message. First validates a
#    joining user's name and sends them the list of users.
#    """
#    message = message[0]
#    room = get_object_or_404(ChatRoom, id=message["room"])
#    if message["action"] == "start":
#        user, created = room.users.get_or_create(name=strip_tags(message["name"]))
#        if not created:
#            socket.send({"action": "in-use"})
#        else:
#            context["user"] = user
#            users = [u.name for u in room.users.exclude(id=user.id)]
#            socket.send({"action": "started", "users": users})
#            user.session = socket.session.session_id
#            user.save()
#            joined = {"action": "join", "name": user.name, "id": user.id}
#            socket.send_and_broadcast_channel(joined)
#    else:
#        try:
#            user = context["user"]
#        except KeyError:
#            return
#        if message["action"] == "message":
#            message["message"] = strip_tags(message["message"])
#            message["name"] = user.name
#            socket.send_and_broadcast_channel(message)

#@events.on_finish(channel="^room-")
#def finish(request, socket, context):
#    """
#    Event handler for a socket session ending in a room. Broadcast
#    the user leaving and delete them from the DB.
#    """
#    try:
#        user = context["user"]
#    except KeyError:
#        return
#    socket.broadcast_channel({"action": "leave", "name": user.name, "id": user.id})
#    user.delete()
#
#def rooms(request, template="rooms.html"):
#    """
#    Homepage - lists all rooms.
#    """
#    context = {"rooms": ChatRoom.objects.all()}
#    return render(request, template, context)
#
#def room(request, slug, template="room.html"):
#    """
#    Show a room.
#    """
#    context = {"room": get_object_or_404(ChatRoom, slug=slug)}
#    return render(request, template, context)
#
#def create(request):
#    """
#    Handles post from the "Add room" form on the homepage, and
#    redirects to the new room.
#    """
#    name = request.POST.get("name")
#    if name:
#        room, created = ChatRoom.objects.get_or_create(name=name)
#        return redirect(room)
#    return redirect(rooms)

@user_passes_test(lambda user: user.is_staff)
def system_message(request, template="system_message.html"):
    return HttpResponse('he go!')
    #context = {"rooms": ChatRoom.objects.all()}
    #if request.method == "POST":
    #    room = request.POST["room"]
    #    data = {"action": "system", "message": request.POST["message"]}
    #    try:
    #        if room:
    #            broadcast_channel(data, channel="room-" + room)
    #        else:
    #            broadcast(data)
    #    except NoSocket, e:
    #        context["message"] = e
    #    else:
    #        context["message"] = "Message sent"
    #return render(request, template, context)