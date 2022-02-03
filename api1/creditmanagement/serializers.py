from rest_framework import serializers
from .models import ledger
from .models import ledgerTransactions
class createLedger(serializers.ModelSerializer):
    class Meta:
        model= ledger
        fields='__all__'
class creditrating(serializers.ModelSerializer):
    class Meta:
        model=ledger
        fields = ['business_id','company_id','credit_rating']

class transactions(serializers.ModelSerializer):
    class Meta:
        model=ledger
        fields = ['credit_balance','credit_outstanding', 'credit_limit','credit_rating']

class EditLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model=ledger
        fields=['enabled','credit_rating','credit_limit']
