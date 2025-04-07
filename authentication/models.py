from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ('consumer', 'Consumer'),
        ('farmer', 'Farmer'),
    )
    
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)  # ✅ Added phone field
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='consumer')

    # Customize groups and permissions
    groups = models.ManyToManyField(
        Group,
        related_name="%(app_label)s_%(class)s_groups",
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="%(app_label)s_%(class)s_user_permissions",
        blank=True
    )

    def __str__(self):
        return self.username
