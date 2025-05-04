from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, default='user')


# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
#
# class UserManager(BaseUserManager):
#     def create_user(self, name, password=None, role='user'):
#         if not name:
#             raise ValueError('Users must have a name')
#         user = self.model(name=name, role=role)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, name, password, role='admin'):
#         user = self.create_user(name=name, password=password, role=role)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save(using=self._db)
#         return user
#
# class User(AbstractBaseUser, PermissionsMixin):
#     name = models.CharField(max_length=100, unique=True)
#     role = models.CharField(max_length=50)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#
#     objects = UserManager()
#
#     USERNAME_FIELD = 'name'
#
#     def __str__(self):
#         return self.name
