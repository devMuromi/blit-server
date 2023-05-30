from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins

from rest_framework import permissions
from receipt import permissions as custom_permissions

from receipt.models import Receipt
from receipt.serializers import ReceiptSerializer


class ReceiptCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer


class ReceiptDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [custom_permissions.IsOwner]
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
