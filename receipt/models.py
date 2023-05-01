from django.db import models
from user.models import User


class Receipt(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="receipts/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data = models.JSONField(null=True)
