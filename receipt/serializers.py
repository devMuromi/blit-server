from rest_framework import serializers
from receipt.models import Receipt


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ("id", "image", "uploaded_at", "uploaded_by")
