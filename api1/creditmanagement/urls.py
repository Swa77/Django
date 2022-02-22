from django.urls import path
from . import views
from . views import createledger
from . views import Transaction

#everything after 8000/ is a pattern and we should give here through urlpatterns

urlpatterns=[
path('createledger/',createledger.as_view()),
path('listledger/',views.listLedger),
path('listledger/<int:bus_id>/', views.listLedger),
path('editledger/<int:key>', views.EditLedger),
#path('transact/',views.transactions),
path('transact/<str:type>/',Transaction.as_view()),
path('filtering_by_credit_rating',views.filtering_by_credit_rating)
]
