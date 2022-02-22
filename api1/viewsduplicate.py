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



class Transaction(APIView):
    def post(self,request,type):
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

                new_balance=credit_balance+transaction_amount
                c_outstanding=0
                if credit_outstanding>=transaction_amount:
                    c_outstanding=credit_outstanding-transaction_amount
                elif credit_outstanding!=0:
                    c_outstanding =0
                for object in ledgers:
                    object.credit_balance = new_balance
                    object.credit_outstanding = c_outstanding
                    object.save()

                ledgertable=ledgerTransactions(ledger_id=ledgers[0],transaction_amount=transaction_amount,credit_balance=new_balance,credit_outstanding=credit_outstanding)
                ledgertable.save()

                ledgeractionsTable= ledgerActionTypes(name="Credit", description="Amount credited")
                ledgeractionsTable.save()

                ledger_action_id = (ledgerActionTypes.objects.last()).id
                action_type_id = ledgerActionTypes.objects.filter(id=ledger_action_id)

                ledgeractions = ledgerActions(ledger_id=ledgers[0], action_type_id=action_type_id[0], prev_value=credit_balance,
                                    current_value=new_balance)
                ledgeractions.save()

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
                        for object in ledgers:
                            object.credit_balance = new_amount
                            object.credit_outstanding = new_credit_outstanding
                            object.save()
                        ledgerTable = ledgerTransactions(ledger_id=ledgers[0], transaction_amount=transaction_amount, credit_balance=new_amount,
                                                 credit_outstanding=new_credit_outstanding)
                        ledgerTable.save()

                        ledgeractionsTable = ledgerActionTypes(name="Debit", description="Amount debited")
                        ledgeractionsTable.save()

                        ledger_actiontype_id = (ledgerActionTypes.objects.last()).id
                        action_type_id = ledgerActionTypes.objects.filter(id=ledger_actiontype_id)

                        ledgeractions = ledgerActions(ledger_id=ledgers[0], action_type_id=action_type_id[0], prev_value=credit_balance,
                                            current_value=new_amount)
                        ledgeractions.save()

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
