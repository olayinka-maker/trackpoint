from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, default='default@example.com')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position} -{self.email}"


class AssetType(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name


class Asset(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('in use ', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
    ]

    name = models.CharField(max_length=200)
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Staff,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True)
    serial_number = models.CharField(max_length=100, unique=True)
    purchase_date = models.DateField(null=True, blank=True)
    time_stamp = models.DateTimeField(default=timezone.now)

    purchase_price = models.DecimalField(max_digits=10,
                                         decimal_places=2,
                                         null=True,
                                         blank=True)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"
