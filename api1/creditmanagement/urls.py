from django.urls import path
from . import views

#everything after 8000/ is a pattern and we should give here through urlpatterns

urlpatterns=[
path('createledger/',views.createledger),
path('listledger/',views.listLedger),
path('listledger/<int:bus_id>/', views.listLedger),
path('editledger/<int:key>', views.EditLedger),
#path('transact/',views.transactions),
path('transact/<str:type>/',views.Transaction),
path('filtering_by_credit_rating',views.filtering_by_credit_rating)
]
