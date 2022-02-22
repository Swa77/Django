from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse #whenever we get request, we are expectng a response
from .models import ledger, distributor, store  # because you want to do crud operations on this
from .models import  ledgerTransactions
from .models import ledgerActions
from .models import ledgerActionTypes
import json
from .serializers import createLedger
from .serializers import EditLedgerSerializer
from .serializers import transactions
from .serializers import creditrating
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
# Create your views here.

@api_view(['GET'])
def listLedger(request,bus_id=None):
    if request.method=='GET':
        if bus_id is None:
            print("here")
            obj=ledger.objects.all()
            serializer=createLedger(obj,many=True)
            return Response(serializer.data)
        if bus_id is not None:
            objs=ledger.objects.filter(business_id=bus_id).count()
            if objs>0:
                print("here")
                obj1=ledger.objects.filter(business_id=bus_id)
                serializers=createLedger(obj1,many=True)
                return Response(serializers.data)
            else:
                return Response({"No such object man!"})
@api_view(['PATCH'])
def EditLedger(request,key):
    if request.method=='PATCH':
        l=ledger.objects.get(id=key)
        serializer=EditLedgerSerializer(l,data=request.data,partial=True)
        if serializer.is_valid():

            serializer.save()
            s=createLedger(l)
            return Response(s.data)


class createledger(APIView):
    def post(self,request):
        data=request.data #json
        tenant_id=request.GET.get('tenant_id')
        distributor_id=data['distributor_id']
        store_id=data['store_id']
        enabled = data['enabled']
        credit_rating = data['credit_rating']
        credit_limit = data['credit_limit']
        credit_balance = data['credit_balance']
        credit_outstanding = data['credit_outstanding']
        distributor_object=distributor.objects.get(distributor_id=distributor_id)
        led=ledger(tenant_id=tenant_id,distributor_id=distributor_object,store_id=store_id,enabled=enabled,credit_rating=credit_rating,credit_limit=credit_limit,credit_balance=credit_balance,
                   credit_outstanding=credit_outstanding)
        led.save()
        store_object=store.objects.get(store_id=store_id)
        store_object.distributor_id.add(distributor_object)


        return Response(request.data)


def add(a, b):
    return a+b

def sub(a, b):
    return a-b

CREDIT = 'credit'
DEBIT = 'debit'


class Transaction(APIView):
    def __init__(self, *args, **kwargs):
        self.registry = {
            CREDIT : {
                "type":CREDIT,
                "descrition": "AMOUNT CREDITED",
                "actions":[add, sub]
            },
            DEBIT : {
                "type":DEBIT,
                "descrition": "AMOUNT DEBITED",
                "actions":[sub, add]
            },

    }
    def post(self, request, type):
        self.ledger_id = request.data.get('id')
        self.transaction_amount = request.data.get('transaction_amount')
        self.object = self.registry.get(type)
        print(self.object)
        return self.execute(request)

    def execute(self, request, *args, **kwargs):
        result, object = self.validate_trasaction()
        if not result:
            return Response(object)
        result, message = self.update_db()
        return Response(message)


    def validate_trasaction(self):
        ledger_count = ledger.objects.filter(id=self.ledger_id).count()
        if ledger_count > 0:
            self.ledgers = ledger.objects.filter(id=self.ledger_id)
            serializer = transactions(self.ledgers, many=True)
            self.credit_limit = serializer.data[0]["credit_limit"]
            self.credit_outstanding = serializer.data[0]["credit_outstanding"]
            self.credit_balance = serializer.data[0]["credit_balance"]
            actions = self.object.get("actions")
            self.new_balance = actions[0](self.credit_balance, self.transaction_amount)
            c_outstanding = 0
            if self.credit_outstanding >= self.transaction_amount:
                self.c_outstanding = actions[1](self.credit_outstanding, self.transaction_amount)
                return (True, self.ledgers)
            else:
                return (None, "No Credit amount")

        return (None, "No Ledger found")


    def update_db(self):

            for object in self.ledgers:
                object.credit_balance = self.new_balance
                object.credit_outstanding = self.c_outstanding
                object.save()
            ledgertable=ledgerTransactions(ledger_id=self.ledgers[0], transaction_amount=self.transaction_amount, credit_balance=self.new_balance, credit_outstanding=self.credit_outstanding)
            ledgertable.save()
            return (True, "Success")


@api_view(['GET'])
def filtering_by_credit_rating(request):
    if request.method=='GET':
        l = ledger.objects.filter(credit_rating__gte=5)
        serializer=creditrating(l,many=True)
        return Response(serializer.data)
