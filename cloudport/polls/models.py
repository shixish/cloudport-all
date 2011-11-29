from django.db import models

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

#class Choice(models.Model):
#    poll = models.ForeignKey(Poll)
#    choice = models.CharField(max_length=200)
#    votes = models.IntegerField()
#class Employee(models.Model):
#    name=models.Charfield(max_length = 100)
#    manager = models.ForeignKey("Self", blank =true,null =true)
#    department=models.FreignKey("department")
#class Department(models.Model):
#    hod =models.ForeignKey("Employee")
#    name= models.CharField(max_Lenght = 100)
#class EmployeeHistory(models.Model):
#    employee= models.oneToOneField(Employee)
#    date_joined=models.DateField()
#    marital_status =models.BooleanField()
#class Contractors(models.Model):
#    name= models.CharField(max_lenght =100)
#    departments= models.ManyToManyField(Department)
#class EmployeeLeave (models.Model):
#    leave_taken =models.DateField()
#    employee= models.ForeignKey(Employee)
