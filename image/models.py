from django.db import models
from user.models import User


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="images/")
    title = models.CharField(max_length=100, blank=False, null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField("Tag", blank=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, blank=False, null=False)

    def __str__(self):
        return self.name
