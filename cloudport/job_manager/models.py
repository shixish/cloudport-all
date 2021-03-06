from django.db import models
from django import forms
from django.contrib import admin
from django.contrib.auth.models import AnonymousUser

#from cloudport import settings
from cloudport.settings import TASK_UPLOAD_FILE_EXTENSIONS
from cloudport.settings import TASK_UPLOAD_FILE_MAX_SIZE
from django.contrib.auth.models import User
import json
import logging

from django.core.files.storage import FileSystemStorage
fs = FileSystemStorage(location='/var/www-django/media/users')

#class DataFile(models.Model):
#    creator = models.ForeignKey(User, related_name='file_creator')
#    created_on = models.DateTimeField(auto_now_add = True)
#    editor  = models.ForeignKey(User, related_name='file_editor')
#    edited_on  = models.DateTimeField(auto_now = True)
#    
#    file = models.FileField(upload_to="default", storage=fs)
#    #file = models.FileField(upload_to="JOB_UPLOADS")
#    #file = models.FileField(upload_to="jobs_uploads ", storage=fs)
#    
#class DataFileForm(forms.ModelForm):
#    class Meta:
#        model = DataFile
#        exclude = ('creator','editor')
#    
#    def clean_file(self):
#        file = self.cleaned_data['file']
#        
#        #raise forms.ValidationError('File type is not supported')
#        if file:
#            file_type = file.content_type.split('/')[0]
#            extension = file.name.split('.')
#            if len(extension) == 1:
#                raise forms.ValidationError('File type is not supported, a file extention is required.')
#            extension = extension.pop()
#
#            if extension not in TASK_UPLOAD_FILE_EXTENSIONS:
#                raise forms.ValidationError('File extension is not supported (%s)'%extension)
#            
#            #if file_type not in settings.TASK_UPLOAD_FILE_TYPES:
#            #    raise forms.ValidationError('File type is not supported (%s)'%file.content_type
#                
#            if file._size > TASK_UPLOAD_FILE_MAX_SIZE:
#                raise forms.ValidationError('Please keep filesize under %s. Current filesize %s' % (filesizeformat(settings.TASK_UPLOAD_FILE_MAX_SIZE), filesizeformat(file._size)))
#
#        return file


class Job(models.Model):
    creator = models.ForeignKey(User, related_name='job_creator', default=-1)
    created_on = models.DateTimeField(auto_now_add = True)
    editor  = models.ForeignKey(User, related_name='job_editor', default=-1)
    edited_on  = models.DateTimeField(auto_now = True)

    status = models.IntegerField(editable=False, default=0)
    filename = models.CharField(max_length = 100)
    output = models.CharField(editable=False, max_length = 100)
    #file = models.FileField(upload_to="JOB_UPLOADS")
    
    def __unicode__(self):
        return self.filename
    
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('creator','editor')

#class JobAdmin(admin.ModelAdmin):
#    #form = JobForm
#    def save_model(self, request, instance, form, change):
#        user = request.user 
#        instance = form.save(commit=False)
#        if not change or not instance.creator:
#            instance.creator = user
#        instance.editor = user
#        instance.save()
#        form.save_m2m()
#        return instance
#    #def save_model(self, request, obj, form, change):
#    #    logging.debug("I AM HERE! LOOK AT ME!! I NEED ATTENTION")
#    #    obj.creator = request.user
#    #    obj.editor = request.user
#    #    obj.save()
#
#admin.site.register(Job, JobAdmin)

class Setting(models.Model):
    setting_name = models.CharField(max_length = 255)
    setting_value = models.CharField(max_length = 255)

