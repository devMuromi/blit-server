from rest_framework import serializers
from receipt.models import Receipt
from datetime import datetime


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ("id", "image", "uploaded_at", "uploaded_by")

    def create(self, validated_data):
        image = validated_data.pop("image")
        receipt = super().create(validated_data)
        day = datetime.now().strftime("%Y%m%d")
        receipt.image.save(f"{day}-{receipt.id}.jpg", image)
        receipt.save()
        return receipt
