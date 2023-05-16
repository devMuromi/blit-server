from django.shortcuts import render
from rest_framework import generics
from receipt.models import Receipt
from receipt.serializers import ReceiptSerializer
from receipt import permissions as custom_permissions
from rest_framework import permissions


class ReceiptList(generics.ListCreateAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer


class ReceiptDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [custom_permissions.IsOwner]
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
