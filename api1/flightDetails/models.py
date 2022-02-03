from django.db import models

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    email=models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.name

class Flight(models.Model):
    flightname=models.CharField(max_length=50)
    name=models.ForeignKey(Customer,on_delete=models.CASCADE)
    Status=(('Confirmed','Confirmed'),('Pending','Pending'))
    status=models.CharField(max_length=50,choices=Status)
    
