from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Scheme, CustomUser, UserActivity
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings




def index(request):
    schemes = Scheme.objects.all()
    scheme_type = request.GET.get('scheme_type')  # Filter by scheme type
    sector = request.GET.get('sector')  # Filter by sector
    search_query = request.GET.get('search', '')  # Search query
    lang = request.GET.get('lang', 'en')  # Default language is English

    # Apply filters if query parameters are provided
    if scheme_type:
        schemes = schemes.filter(scheme_type=scheme_type)
    if sector:
        schemes = schemes.filter(sector=sector)
    if search_query:
        schemes = schemes.filter(name_en__icontains=search_query)  # Search by name in English
        
    print(schemes)

    # Pass the filtered schemes and language to the templa  te
    return render(request, 'index.html', {
        'schemes': schemes,
        'lang': lang,
        'search_query': search_query,
        'scheme_type': scheme_type,
        'sector': sector,
    })

def about(request):
    return render(request, 'About_Us.html')
def contact(request):
    return render(request, 'Contact_Us.html')
def privacy_policy(request):
    return render(request, 'under_construction.html')
def terms_and_conditions(request):
    return render(request, 'under_construction.html')
def faqs(request):
    return render(request, 'under_construction.html')   
def team(request):
    return render(request, 'Our_Team.html')
def under_construction(request):
    return render(request, 'under_construction.html')
def log_user_activity(user, activity_type, description, created_by=None):
        UserActivity.objects.create(
            user=user,
            activity_type=activity_type,
            description=description,
            created_by=created_by or user
        )
def scheme_detail(request, scheme_id):
    scheme = get_object_or_404(Scheme, id=scheme_id)
    lang = request.GET.get('lang', 'en')
    return render(request, 'scheme_detail.html', {'scheme': scheme, 'lang': lang})

def is_admin(user):
    return user.is_superuser or user.role == 'admin'

def is_staff_user(user):
    return user.role == 'staff'


@login_required
#@user_passes_test(lambda u: u.is_superuser or u.is_staff_user)
def add_scheme(request):
    if request.method == 'POST':
        name_en = request.POST.get('name_en')
        name_mr = request.POST.get('name_mr')
        scheme_type = request.POST.get('scheme_type')
        sector = request.POST.get('sector')
        summary_en = request.POST.get('summary_en')
        summary_mr = request.POST.get('summary_mr')
        details_en = request.POST.get('details_en')
        details_mr = request.POST.get('details_mr')
        photo = request.FILES.get('photo')
        eligibility_criteria_en = request.POST.get('eligibility_criteria_en')
        eligibility_criteria_mr = request.POST.get('eligibility_criteria_mr')
        is_active = request.POST.get('is_active') == 'on'
        website_link = request.POST.get('website_link')

        # Check required fields
        if not all([name_en, name_mr, scheme_type, sector, summary_en, eligibility_criteria_en, eligibility_criteria_mr]):
            messages.error(request, "Please fill all required fields.")
        else:
            Scheme.objects.create(
                name_en=name_en,
                name_mr=name_mr,
                scheme_type=scheme_type,
                sector=sector,
                summary_en=summary_en,
                summary_mr=summary_mr,
                details_en=details_en,
                details_mr=details_mr,
                photo=photo,
                eligibility_criteria_en=eligibility_criteria_en,  # Fixed typo
                eligibility_criteria_mr=eligibility_criteria_mr,
                is_active=is_active,
                website_link=website_link,
                created_by=request.user
            )
            # Log user activity
            log_user_activity(
                user=request.user,
                activity_type="Scheme Addition",
                description=f"Scheme '{name_en}' has been added by '{request.user.username}'.",
                created_by=request.user
            )
            messages.success(request, "Scheme added successfully!")
            return redirect('index')

    return render(request, 'add_scheme.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        full_name = request.POST.get('Fname')
        email = request.POST.get('email')
        role = request.POST.get('role')

        if not all([username, password1, password2, full_name, email, role]):
            messages.error(request, "Please fill all required fields.")
        elif password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif role == 'staff':
            user = CustomUser.objects.create_user(
                username=username,
                password=password1,
                full_name=full_name,
                role=role,
                email=email,
                is_active=False  # Awaiting approval
            )

            # ✅ Send Email
            send_mail(
                subject="Staff Registration Acknowledgment",
                message=(
                    f"Dear {full_name},\n\n"
                    "Thank you for registering as a staff member with our platform.\n\n"
                    "We have received your application and it is currently under review by our administrative team. "
                    "You will be notified via email once your account has been approved or if further information is required.\n\n"
                    "If you have any questions or need assistance in the meantime, please feel free to contact our support team.\n\n"
                    "Thank you for your interest and we look forward to having you on board.\n\n"
                    "Best regards,\n"
                    "The Administration Team"
                ),
                from_email=None,  # Uses DEFAULT_FROM_EMAIL
                recipient_list=[email],
                fail_silently=False,
            )
            # if role == 'staff':
            #     admin_users = CustomUser.objects.filter(role='admin')
            #     admin_emails = [admin.email for admin in admin_users if admin.email]

            #     send_mail(
            #         subject="New Staff Registration Pending Approval",
            #         message=(
            #             f"Dear Admin,\n\n"
            #             f"A new staff registration request has been submitted by {full_name}.\n\n"
            #             "Please log in to the admin panel to review and approve the application.\n\n"
            #             "Best regards,\n"
            #             "The Administration Team"
            #         ),
            #         from_email=None,  # Uses DEFAULT_FROM_EMAIL
            #         recipient_list=admin_emails,  # Send to all admin emails
            #         fail_silently=False,
            #     )

            messages.success(request, "User registered successfully! Awaiting admin approval.")
            return redirect('/login/')

        elif role == 'admin':
            user = CustomUser.objects.create_superuser(
                username=username,
                password=password1,
                full_name=full_name,
                role=role,
                email=email
            )
            messages.success(request, "Admin registered successfully!")
            return redirect('/login/')
        else:
            messages.error(request, "Invalid role selected.")

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                messages.error(request, "Your account is awaiting admin approval.")
                return redirect('/login/')
            login(request, user)
            if user.role == 'admin':
                return redirect('/admin_user/')
            elif user.role == 'staff':
                return redirect('/staff_user/')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


@login_required
@user_passes_test(is_admin, login_url='login_view')
def admin_user(request):
    user_activities = UserActivity.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'Admin-dashboard.html', {'user_activities': user_activities})

def staff_user_approval(request):
    pending_users = CustomUser.objects.filter(is_active=False, role='staff')
    return render(request, 'Pending_Approval.html', {'pending_users': pending_users})

@login_required
@user_passes_test(is_admin, login_url='login_view')
def activate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f"User '{user.username}' has been Approved.")
    return redirect('staff_user_approval')

@login_required
@user_passes_test(is_admin, login_url='login_view')
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, f"User '{user.username}' has been rejected")
    return redirect('Pending_Approval.html')

@login_required
@user_passes_test(is_staff_user, login_url='login_view')
def staff_user(request):        
    user_activities = UserActivity.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'Staff.html', {'user_activities': user_activities})

@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('/')  # Redirect to the login page after logout

def manage_scheme(request):
    schemes = Scheme.objects.all()
    return render(request, 'manage_scheme.html', {'schemes': schemes})

def update_scheme(request,scheme_id):
    scheme = get_object_or_404(Scheme, id=scheme_id)
    lang = request.GET.get('lang', 'en')
    if request.method == 'POST':
        scheme.name_en = request.POST.get('name_en', scheme.name_en)
        scheme.name_mr = request.POST.get('name_mr', scheme.name_mr)
        scheme.scheme_type = request.POST.get('scheme_type', scheme.scheme_type)
        scheme.sector = request.POST.get('sector', scheme.sector)
        scheme.summary_en = request.POST.get('summary_en', scheme.summary_en)
        scheme.summary_mr = request.POST.get('summary_mr', scheme.summary_mr)
        scheme.details_en = request.POST.get('details_en', scheme.details_en)
        scheme.details_mr = request.POST.get('details_mr', scheme.details_mr)
        scheme.website_link = request.POST.get('website_link', scheme.website_link)
        scheme.is_active = request.POST.get('is_active') == 'on'
        scheme.eligibility_criteria_en = request.POST.get('eligibility_criteria_en', scheme.eligibility_criteria_en)
        scheme.eligibility_criteria_mr = request.POST.get('eligibility_criteria_mr', scheme.eligibility_criteria_mr)

        
        
        if 'photo' in request.FILES:
            scheme.photo = request.FILES['photo']

        scheme.save()
          # Log user activity
        log_user_activity(
            user=request.user,
            activity_type="Scheme Update",
            description=f"Scheme '{scheme.name_en}' has been updated by '{request.user.username}'.",
            created_by=request.user
        )
        messages.success(request, "Scheme updated successfully!")
        return redirect('manage_scheme')
    return render(request, 'update_scheme.html', {'scheme': scheme, 'lang': lang})

def delete_scheme(request, scheme_id):
    scheme = get_object_or_404(Scheme, id=scheme_id)
    scheme.delete()
    # Log user activity
    log_user_activity(
        user=request.user,
        activity_type="Scheme Deletion",
        description=f"Scheme '{scheme.name_en}' has been deleted by '{request.user.username}'.",
        created_by=request.user
    )
    return redirect('manage_scheme')  # make sure this URL name exists in your urls.py

@login_required
@user_passes_test(is_admin)  # Your custom admin role checker
def scheme_history_view(request, scheme_id):
    scheme = get_object_or_404(Scheme, id=scheme_id)
    history = scheme.history.all().order_by('-history_date')

    return render(request, 'scheme_history.html', {
        'scheme': scheme,
        'history': history,
    })
    
def send_test_email():
    send_mail(
        subject="Test Email",
        message="This is a test email from Django using Anymail + Gmail!",
        from_email="codehack584@gmail.com",
        recipient_list=["karamoberoi19@gmail.com"],
        fail_silently=False,
    )
    
def user_profile_edit(request):
    user = request.user
    if request.method == 'POST':
        user.full_name = request.POST.get('full_name', user.full_name)
        user.email = request.POST.get('email', user.email)
        user.role = request.POST.get('role', user.role)

        # # If the password is provided, update it
        # if request.POST.get('password'):
        #     user.set_password(request.POST.get('password'))

        user.save()
        messages.success(request, "Profile updated successfully!")
        if user.role == 'staff':
            return redirect('/staff_user/')
        elif user.role == 'admin':
            return redirect('/admin_user/')

    return render(request,{'user': user})