from django.contrib import admin
from .models import ledger
from .models import ledgerTransactions
from .models import ledgerActions
from .models import ledgerActionTypes
from .models import distributor
from .models import store
# Register your models here.
admin.site.register(ledger)
admin.site.register(ledgerTransactions)
admin.site.register(ledgerActions)
admin.site.register(ledgerActionTypes)
admin.site.register(distributor)
admin.site.register(store)
