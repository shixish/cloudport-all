#added by andrew
from django import forms
from django.shortcuts import render_to_response
from django.template.defaultfilters import filesizeformat
from django.conf import settings

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()
    
    def clean_file(self):
        file = self.cleaned_data['file']
        
        #raise forms.ValidationError('File type is not supported')
        if file:
            file_type = file.content_type.split('/')[0]
            extension = file.name.split('.')
            if len(extension) == 1:
                raise forms.ValidationError('File type is not supported, a file extention is required.')
            extension = extension.pop()

            #We dont need to block file extensions anymore
            #if extension not in settings.TASK_UPLOAD_FILE_EXTENSIONS:
            #    raise forms.ValidationError('File extension is not supported (%s)'%extension)
            
            #if file_type not in settings.TASK_UPLOAD_FILE_TYPES:
            #    raise forms.ValidationError('File type is not supported (%s)'%file.content_type
                
            if file._size > settings.TASK_UPLOAD_FILE_MAX_SIZE:
                raise forms.ValidationError('Please keep filesize under %s. Current filesize %s' % (filesizeformat(settings.TASK_UPLOAD_FILE_MAX_SIZE), filesizeformat(file._size)))

        return file
