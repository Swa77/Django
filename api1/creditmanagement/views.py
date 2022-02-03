from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse #whenever we get request, we are expectng a response
from .models import ledger#because you want to do crud operations on this
from .models import  ledgerTransactions
from .models import ledgerActions
from .models import ledgerActionTypes
import json
from .serializers import createLedger
from .serializers import EditLedgerSerializer
from .serializers import transactions
from .serializers import creditrating
from rest_framework.decorators import api_view
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
@api_view(['POST'])
def createledger(request):
    if request.method=='POST':
        serializer= createLedger(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

@api_view(['POST'])
def Transaction(request,type):
    if request.method=='POST':
        if type=="credit":
            ledger_id=request.data.get('id')
            transaction_amount=request.data.get('transaction_amount')
            ledger_count = ledger.objects.filter(id=ledger_id).count()
            if ledger_count>0:
                ledgers=ledger.objects.filter(id=ledger_id)
                serializer=transactions(ledgers,many=True)
                credit_limit=serializer.data[0]["credit_limit"]
                credit_outstanding=serializer.data[0]["credit_outstanding"]
                credit_balance = serializer.data[0]["credit_balance"]
                if credit_outstanding+transaction_amount>credit_limit:
                    return Response({"Cannot be done"})
                new_balance=credit_balance+transaction_amount
                c_outstanding=0
                if credit_outstanding>=transaction_amount:
                    c_outstanding=credit_outstanding-transaction_amount
                elif credit_outstanding!=0:
                    c_outstanding =0
                for ob in ledgers:
                    ob.credit_balance = new_balance
                    ob.credit_outstanding = c_outstanding
                    ob.save()
                ledgertable=ledgerTransactions(ledger_id=ledgers[0],transaction_amount=transaction_amount,credit_balance=new_balance,credit_outstanding=credit_outstanding)
                ledgertable.save()
                a_id = (ledgerActionTypes.objects.last()).id
                print(a_id)
                ledgeractionsTable= ledgerActionTypes(name="Credit", description="Amount credited")
                ledgeractionsTable.save()

                return Response({"Success"})
            else:
                return Response({"Ledger id not found"})

        elif type == "debit":
            ledger_id = request.data.get('id')
            transaction_amount = request.data.get('transaction_amount')
            ledger_count = ledger.objects.filter(id=ledger_id).count()
            if ledger_count > 0:
                ledgers = ledger.objects.filter(id=ledger_id)
                serializer = transactions(ledgers, many=True)
                credit_limit = serializer.data[0]["credit_limit"]
                credit_outstanding = serializer.data[0]["credit_outstanding"]
                credit_balance = serializer.data[0]["credit_balance"]
                if transaction_amount <= credit_balance:
                    new_amount = credit_balance - transaction_amount
                    total_outstanding = credit_outstanding + transaction_amount
                    if total_outstanding <= credit_limit:
                        new_credit_outstanding = credit_outstanding + transaction_amount
                        for ob in ledgers:
                            ob.credit_balance = new_amount
                            ob.credit_outstanding = new_credit_outstanding
                            ob.save()
                        ledgerTable = ledgerTransactions(ledger_id=ledgers[0], transaction_amount=transaction_amount, credit_balance=new_amount,
                                                 credit_outstanding=new_credit_outstanding)
                        ledgerTable.save()
                        ledgeractionsTable = ledgerActionTypes(name="Debit", description="Amount debited")
                        ledgeractionsTable.save()
                        return Response({"Success"})
                    else:
                        return Response({"Credit limit exceeded"})
                else:
                    return Response({"Amount not sufficient"})
            else:
                return Response({"Ledger id not found"})
@api_view(['GET'])
def filtering_by_credit_rating(request):
    if request.method=='GET':
        l = ledger.objects.filter(credit_rating__gte=5)
        serializer=creditrating(l,many=True)
        return Response(serializer.data)
