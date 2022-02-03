from django.db import models

# Create your models here.
class ledger(models.Model):
    company_id=models.CharField(max_length=100)
    business_id=models.CharField(max_length=100)
    customer_id=models.CharField(max_length=100)
    enabled=models.BooleanField()
    credit_rating=models.PositiveIntegerField()
    credit_limit=models.PositiveIntegerField()
    credit_balance=models.IntegerField()
    credit_outstanding=models.IntegerField()
    class Meta:
        unique_together = (("company_id", "business_id","customer_id"),)
    def __str__(self):
        return self.company_id

class ledgerTransactions(models.Model):
    ledger_id=models.ForeignKey(ledger,on_delete=models.CASCADE)
    transaction_amount=models.PositiveIntegerField()
    credit_balance=models.IntegerField()
    credit_outstanding=models.IntegerField()
class ledgerActions(models.Model):
    ledger_id = models.ForeignKey(ledger,on_delete=models.CASCADE)
    action_type_id=models.PositiveIntegerField()
    prev_value=models.PositiveIntegerField()
    current_value=models.PositiveIntegerField()
class ledgerActionTypes(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
