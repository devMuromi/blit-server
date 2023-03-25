from django.shortcuts import render
from rest_framework import generics
from receipt.models import Receipt
from receipt.serializers import ReceiptSerializer


class ReceiptList(generics.ListCreateAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer


class ReceiptDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
