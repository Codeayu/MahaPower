from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Custom user model to handle admin and staff roles
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ]
    full_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    Role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')

    def _str_(self):
        return self.username

# Main model for storing schemes
class Scheme(models.Model):
    SCHEME_TYPES = [
        ('Loan', 'Loan'),
        ('Skill', 'Skill Development'),
        ('Funding', 'Startup Funding'),
    ]

    SECTORS = [
        ('Agriculture', 'Agriculture'),
        ('Manufacturing', 'Manufacturing'),
        ('Services', 'Services'),
        ('Other', 'Other'),
    ]

    name_en = models.CharField(max_length=200)
    name_mr = models.CharField(max_length=200)
    scheme_type = models.CharField(max_length=20, choices=SCHEME_TYPES)
    sector = models.CharField(max_length=50, choices=SECTORS)
    summary_en = models.TextField()
    summary_mr = models.TextField()
    details_en = models.TextField()
    details_mr = models.TextField()
    website_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='scheme_photos/', blank=True, null=True)
    eligibility_criteria_en = models.TextField(blank=True, null=True, default="")
    eligibility_criteria_mr = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name_en
