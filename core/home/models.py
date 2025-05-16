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
    otp = models.CharField(max_length=6, null=True, blank=True)    
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
            




# distric model for storing district information
class District(models.Model):
    name_en = models.CharField(max_length=100)
    name_mr = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_en
    
#taluka model for storing taluka information
class Taluka(models.Model):
    name_en = models.CharField(max_length=100)
    name_mr = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='talukas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_en

#panchayat model for storing panchayat information
class GramPanchayat(models.Model):
    name_en = models.CharField(max_length=100)
    name_mr = models.CharField(max_length=100)
    taluka = models.ForeignKey(Taluka, on_delete=models.CASCADE, related_name='grampanchayats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_en
class Sector(models.Model):
    name_en = models.CharField(max_length=100)
    name_mr = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.name_en

    # worktype model for storing worktype information
class WorkType(models.Model):
    name_en = models.CharField(max_length=255)
    name_mr = models.CharField(max_length=255)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='work_types')
    created_at = models.DateTimeField(default=timezone.now)                                    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.name_en
# worksuggestions model for storing work suggestions
# Work suggestions assigned to each GP
class WorkSuggestion(models.Model):
    gram_panchayat = models.ForeignKey(GramPanchayat, on_delete=models.CASCADE)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE)
    is_specialty = models.BooleanField(default=False)  # Indicates if this work type is a specialty for this GP
    
    def __str__(self):
        specialty_indicator = " (Specialty)" if self.is_specialty else ""
        return f"{self.gram_panchayat.name} → {self.work_type.name_en}{specialty_indicator}"