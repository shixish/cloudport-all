from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from cloudport.job_manager.models import Job

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        #excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        fields = ['username', 'first_name', 'last_name', 'last_login', 'id']
        #authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class JobResource(ModelResource):
    editor = fields.ForeignKey(UserResource, 'editor')
    
    class Meta:
        queryset = Job.objects.all()
        resource_name = 'job'
        #authentication = BasicAuthentication()
        authorization = DjangoAuthorization()