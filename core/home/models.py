from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from simple_history.models import HistoricalRecords


# Custom user model to handle admin and staff roles
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    ]

    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')
    history = HistoricalRecords()

    def __str__(self):
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
    history = HistoricalRecords()

    def __str__(self):
        return self.name_en
        # Model to track user activities
class UserActivity(models.Model):
            user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
            activity_type = models.CharField(max_length=100)  # e.g., Login, Logout, Data Update
            description = models.TextField(blank=True, null=True)  # Detailed description of the activity
            # ip_address = models.GenericIPAddressField(blank=True, null=True)  # IP address of the user
            # user_agent = models.TextField(blank=True, null=True)  # Browser or device details
            # location = models.CharField(max_length=255, blank=True, null=True)  # Geographical location if available
            timestamp = models.DateTimeField(default=timezone.now)  # When the activity occurred
            created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_created_by')  # Who triggered the activity
            updated_at = models.DateTimeField(auto_now=True)  # Last updated timestamp

            def __str__(self):
                return f"{self.user.username} - {self.activity_type} at {self.timestamp}"