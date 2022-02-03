from django.contrib import admin
from .models import ledger
from .models import ledgerTransactions
from .models import ledgerActions
from .models import ledgerActionTypes
# Register your models here.
admin.site.register(ledger)
admin.site.register(ledgerTransactions)
admin.site.register(ledgerActions)
admin.site.register(ledgerActionTypes)
