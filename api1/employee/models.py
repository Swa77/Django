from django.db import models
from datetime import datetime,date
# Create your models here.
class Jobprofile(models.Model): #you need to add this model in admin site
    name=models.CharField(max_length=50)
    employeecode=models.CharField(max_length=50,null=True)
    designation=models.CharField(max_length=100,null=True)
    experience=models.IntegerField(default=0,null=True,blank=True)
    company=models.CharField(max_length=50,null=True,blank=True)
    logo=models.ImageField(upload_to='images/',null=True,blank=True)

class Project(models.Model):
    emp_id=models.ForeignKey(Jobprofile,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    project_head=models.CharField(max_length=50)
    deadline=models.DateField(auto_now_add=False,auto_now=False,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

