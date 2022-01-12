from django.shortcuts import render
from django.http import HttpResponse #whenever we get request, we are expectng a response
from .models import Jobprofile #because you want to do crud operations on this
import json
from django.views.decorators.csrf import csrf_exempt
# write api's here
def index(request): #It is kike api, and we should give path in urls.py
    return render(request,'api1/index.html')
@csrf_exempt
def getdetails(request):
    if request.method=="GET":
        result=[]
        jobs=Jobprofile.objects.all()

        for k in jobs:
            data={
            "Name":k.name,
            "Company":k.company
            }
            result.append(data)
        return HttpResponse(json.dumps(result))

    if request.method=="POST":
        body=request.body.decode('utf-8') #whenever we r inserting something, the value will be encoded, therefore we should decode it
        value=json.loads(body)
        company=value['company']
        name=value['name']
        job=Jobprofile(company=company,name=name)
        job.save()
        return HttpResponse({"New data added successfully"})
