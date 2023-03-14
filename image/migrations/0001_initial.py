# Generated by Django 4.1.7 on 2023-03-14 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("image", models.ImageField(upload_to="images/")),
                ("title", models.CharField(max_length=100)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
