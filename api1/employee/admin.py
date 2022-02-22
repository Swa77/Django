from django.contrib import admin
from .forms import Employeeform
from .models import Jobprofile
from .models import Project
# Register your models here.

class Employee(admin.ModelAdmin):
    form = Employeeform
    class Meta:
        model = Jobprofile
    list_display=['name','company']
admin.site.register(Jobprofile)
admin.site.register(Project)
