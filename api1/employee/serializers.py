from rest_framework import serializers
class EmployeeSerializer(serializers.Serializer):
     name=serializers.CharField(max_length=50)
     
     company=serializers.CharField(max_length=50)
