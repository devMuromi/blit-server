# Generated by Django 4.1.7 on 2023-06-28 01:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="kakao_pay_code",
            field=models.CharField(max_length=32, null=True),
        ),
    ]