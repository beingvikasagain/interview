from datetime import datetime

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    User,
)
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name
    

class Task(models.Model):
    status = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task")
    status = models.CharField(max_length=25, choices=status)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.due_date = datetime.strptime(self.due_date, '%Y-%m-%d')
        if self.due_date < datetime.now():
            raise ValueError('due date must be greater than current date')
        super().save(*args, **kwargs)



