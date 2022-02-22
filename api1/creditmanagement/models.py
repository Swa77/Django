from django.db import models

# Create your models here.
class distributor(models.Model):
    distributor_id=models.CharField(max_length=100,null=True)
    tenant_id = models.CharField(max_length=100)
    name=models.CharField(max_length=100)

class store(models.Model):
    store_id= models.CharField(max_length=100,null=True)
    distributor_id = models.ManyToManyField(distributor,null=True)
    tenant_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    owner_name=models.CharField(max_length=100)

class ledger(models.Model):
    tenant_id=models.CharField(max_length=100,null=True)
    distributor_id = models.ForeignKey(distributor, on_delete=models.CASCADE)
    store_id= models.CharField(max_length=100,null=True)
    #business_id=models.CharField(max_length=100)#distributor-freign
    #customer_id=models.CharField(max_length=100)#store table forgn key
    enabled=models.BooleanField()
    credit_rating=models.PositiveIntegerField()
    credit_limit=models.PositiveIntegerField()
    credit_balance=models.IntegerField()
    credit_outstanding=models.IntegerField()



class ledgerTransactions(models.Model):
    ledger_id=models.ForeignKey(ledger,on_delete=models.CASCADE)
    transaction_amount=models.PositiveBigIntegerField()
    credit_balance=models.IntegerField()
    credit_outstanding=models.IntegerField()
class ledgerActionTypes(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
class ledgerActions(models.Model):
    ledger_id = models.ForeignKey(ledger,on_delete=models.CASCADE)
    action_type_id=models.ForeignKey(ledgerActionTypes,on_delete=models.CASCADE)
    prev_value=models.PositiveIntegerField()
    current_value=models.PositiveIntegerField()
