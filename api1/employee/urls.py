from django.urls import path
from . import views

#everything after 8000/ is a pattern and we should give here through urlpatterns

urlpatterns=[
path('employee/',views.index,name='index'),  # name is optional and with this ur api is called, and you should register this api in main urls.py
path('jobs/',views.getdetails),

]
