from django.urls import path
from . import views

#everything after 8000/ is a pattern and we should give here through urlpatterns

urlpatterns=[
path('Flightdetails/',views.index,name='index'),
]
