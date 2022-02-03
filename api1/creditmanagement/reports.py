from django.db.models import Count,Avg,Sum
from creditmanagement.models import ledger

def report():
    qs=ledger.objects.values("company_id").annotate(avg=Avg("credit_rating"))
    return qs
