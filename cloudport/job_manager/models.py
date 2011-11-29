from django.db import models
from django import forms 
from cloudport import settings

import json

class Job(models.Model):
    date_published = models.DateTimeField('date published', auto_now_add=True)
    date_updated = models.DateTimeField('date updated', auto_now=True)
    status = models.IntegerField(editable=False, default=0)
    title = models.CharField(max_length = 100)
    output = models.CharField(editable=False, max_length = 100)
    file = models.FileField(upload_to="JOB_UPLOADS")
    
    def __unicode__(self):
        return self.title
    
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
    
    def clean_file(self):
        file = self.cleaned_data['file']
        
        #raise forms.ValidationError('File type is not supported')
        if file:
            file_type = file.content_type.split('/')[0]
            extension = file.name.split('.')
            if len(extension) == 1:
                raise forms.ValidationError('File type is not supported, a file extention is required.')
            extension = extension.pop()

            if extension not in settings.TASK_UPLOAD_FILE_EXTENSIONS:
                raise forms.ValidationError('File extension is not supported (%s)'%extension)
            
            #if file_type not in settings.TASK_UPLOAD_FILE_TYPES:
            #    raise forms.ValidationError('File type is not supported (%s)'%file.content_type
                
            if file._size > settings.TASK_UPLOAD_FILE_MAX_SIZE:
                raise forms.ValidationError('Please keep filesize under %s. Current filesize %s' % (filesizeformat(settings.TASK_UPLOAD_FILE_MAX_SIZE), filesizeformat(file._size)))

        return file