from rest_framework import serializers
from .models import ledger,store,distributor
from .models import ledgerTransactions

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

class DistributorSerializer(serializers.ModelSerializer):

    class Meta:
        model=distributor
        fields=["distributor_id","name"]
class StoreSerializer(serializers.ModelSerializer):
    #customer_id=transactions(many=True,read_only=True)
    #distributor_id = DistributorSerializer()
    class Meta:
        model=store
        fields=("store_id","name","owner_name")

class createLedger(serializers.ModelSerializer):
    distributor_id=DistributorSerializer()
    #store_id=StoreSerializer()
    class Meta:
        model= ledger
        fields=["distributor_id","store_id","enabled","credit_rating","credit_outstanding","credit_limit","credit_balance"]