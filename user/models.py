from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import UserManager as DjangoUserManager
import random


def generate_unique_id():
    while True:
        id = str(random.randint(100000000000, 999999999999))
        if not User.objects.filter(id=id).exists():
            return id


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, kakao_id, **kwargs):
        if not username:
            raise ValueError("Users must have an username")
        user = self.model(username=username, kakao_id=kakao_id, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, kakao_id, **extra_fields):
        username = generate_unique_id()
        password = self.make_random_password()
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, kakao_id, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, None, **extra_fields)


class User(AbstractUser):
    # username
    first_name = None
    last_name = None
    email = None
    # is_staff
    # is_active
    # date_joined
    kakao_id = models.CharField(max_length=255, unique=True, null=True)

    REQUIRED_FIELDS = []

    objects = UserManager()
