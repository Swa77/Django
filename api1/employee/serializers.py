from rest_framework import serializers
from .models import Project,Jobprofile

class EmployeeSerializer(serializers.ModelSerializer):
    #id=serializers.IntegerField(required=False)
    class Meta:
        model = Jobprofile
        fields= ["name","employeecode","designation","experience","company"]


class create(serializers.ModelSerializer):
    emp_id=EmployeeSerializer()
    class Meta:
        model=Project
        fields=["title","project_head","deadline","created_at","updated_at",'emp_id']
        #depth=1

