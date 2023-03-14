from django.db import models
from user.models import User

# Create your models here.


def upload_to(instance, filename):
    return "images/{filename}".format(filename=filename)


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="images/")
    title = models.CharField(max_length=100, blank=False, null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
