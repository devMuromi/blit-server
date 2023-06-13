from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins

from rest_framework import permissions
from receipt import permissions as custom_permissions

from receipt.models import Receipt
from receipt.serializers import ReceiptSerializer


class ReceiptListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReceiptSerializer

    def get_queryset(self):
        user = self.request.user
        return Receipt.objects.filter(uploaded_by=user)


class ReceiptDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [custom_permissions.IsOwner]
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
