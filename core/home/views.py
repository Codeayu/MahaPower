from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Scheme, CustomUser, UserActivity
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from .models import District, Taluka, GramPanchayat, WorkSuggestion, WorkType




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
    
    # Log user activity
    log_user_activity(
        user=user,
        activity_type="Account Activation",
        description=f"User '{user.username}' account has been activated by {request.user.username}.",
        created_by=request.user
    )
    
    send_mail(
        subject="Account Approval Notification",
        message=(
            f"Dear {user.full_name},\n\n"
            "We are pleased to inform you that your staff account has been approved.\n\n"
            "You can now log in to your account and access the platform using your credentials.\n\n"
            "If you have any questions or require assistance, please do not hesitate to contact our support team.\n\n"
            "Thank you for being a part of our team.\n\n"
            "Best regards,\n"
            "The Administration Team"
        ),
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )
    messages.success(request, f"User '{user.username}' has been Approved.")
    return redirect('staff_user_approval')

@login_required
@user_passes_test(is_admin, login_url='login_view')
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
      # Log user activity
    log_user_activity(
        user=user,
        activity_type="Account Deletion/ Rejection",
        description=f"User '{user.username}' account has been deleted by '{request.user.username}'.",
        created_by=request.user
    )
    send_mail(
        subject="Important: Staff Registration Rejected",
        message=(
            f"Dear {user.full_name},\n\n"
            "We regret to inform you that your application for staff registration has not been approved at this time.\n\n"
            "If you have any questions or require further clarification, please feel free to contact our support team.\n\n"
            "Thank you for your understanding.\n\n"
            "Best regards,\n"
            "The Administration Team"
        ),
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )
    messages.success(request, f"User '{user.username}' has been rejected")
    return redirect('Pending_Approval.html')

@login_required(login_url='/login/')
@user_passes_test(is_staff_user)
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
def password_reset_flow(request):
    step = request.POST.get('step', 'forgot')
    context = {'step': step}

    if step == 'forgot':
        if request.method == 'POST':
            username = request.POST.get('username')
            try:
                user = CustomUser.objects.get(username=username)
                otp = get_random_string(length=6, allowed_chars='0123456789')
                user.otp = otp
                user.save()

                send_mail(
                    subject="Password Reset OTP",
                    message=f"Your OTP for password reset is: {otp}",
                    from_email=None,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                messages.success(request, "OTP sent to your email.")
                context = {'step': 'verify', 'user_id': user.id}
            except CustomUser.DoesNotExist:
                messages.error(request, "User not found.")
                context = {'step': 'forgot'}
        else:
            context = {'step': 'forgot'}

    elif step == 'verify':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id)
        context['user_id'] = user_id
        if request.method == 'POST':
            entered_otp = request.POST.get('otp')
            if entered_otp == user.otp:
                messages.success(request, "OTP verified.")
                context['step'] = 'reset'
            else:
                messages.error(request, "Invalid OTP.")

    elif step == 'reset':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id)
        context['user_id'] = user_id
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 != password2:
                messages.error(request, "Passwords do not match.")
            else:
                user.set_password(password1)
                user.otp = None
                user.save()
                messages.success(request, "Password reset successfully. Please log in.")
                return redirect('/login/')

    return render(request, 'password_reset_flow.html', context)


def get_work_suggestions(request):
    districts = District.objects.all()
    sectors = WorkType.objects.values_list('sector', flat=True).distinct().exclude(sector__isnull=True)

    selected_district = request.GET.get('district')
    selected_taluka = request.GET.get('taluka')
    selected_gp = request.GET.get('gram_panchayat')
    selected_sector = request.GET.get('sector')

    suggestions = None
    if selected_gp:
        suggestions = WorkSuggestion.objects.filter(
            gram_panchayat_id=selected_gp
        ).select_related('work_type')

        if selected_sector:
            suggestions = suggestions.filter(work_type__sector=selected_sector)

    context = {
        'districts': districts,
        'sectors': sectors,
        'suggestions': suggestions,
        'selected_district': selected_district,
        'selected_taluka': selected_taluka,
        'selected_gp': selected_gp,
        'selected_sector': selected_sector,
    }
    return render(request, 'work_suggest.html', context)

def get_suggestions(request):
    selected_gp = request.GET.get('gram_panchayat')
    selected_sector = request.GET.get('sector')
    
    suggestions = []
    if selected_gp:
        query = WorkSuggestion.objects.filter(
            gram_panchayat_id=selected_gp
        ).select_related('work_type')
        
        if selected_sector:
            query = query.filter(work_type__sector=selected_sector)
            
        suggestions = [
            {
                'id': suggestion.id,
                'work_type_name': suggestion.work_type.name_en,
                'sector': suggestion.work_type.sector,
                #'description': suggestion.work_type.description_en
            }
            for suggestion in query
        ]
    
    return JsonResponse({'suggestions': suggestions})


def get_talukas(request):
    district_id = request.GET.get('district_id')
    talukas = Taluka.objects.filter(district_id=district_id).values('id', 'name')
    return JsonResponse(list(talukas), safe=False)


def get_gram_panchayats(request):
    taluka_id = request.GET.get('taluka_id')
    gps = GramPanchayat.objects.filter(taluka_id=taluka_id).values('id', 'name')
    return JsonResponse(list(gps), safe=False)



def manage_suggestions(request):
    districts = District.objects.all()
    sectors = WorkType.objects.values_list('sector', flat=True).distinct().exclude(sector__isnull=True)

    selected_district = request.GET.get('district')
    selected_taluka = request.GET.get('taluka')
    selected_gp = request.GET.get('gram_panchayat')
    selected_sector = request.GET.get('sector')

    suggestions = None
    if selected_gp:
        suggestions = WorkSuggestion.objects.filter(
            gram_panchayat_id=selected_gp
        ).select_related('work_type')

        if selected_sector:
            suggestions = suggestions.filter(work_type__sector=selected_sector)

    context = {
        'districts': districts,
        'sectors': sectors,
        'suggestions': suggestions,
        'selected_district': selected_district,
        'selected_taluka': selected_taluka,
        'selected_gp': selected_gp,
        'selected_sector': selected_sector,
    }
    return render(request, 'manage_suggestions.html', context)
@login_required
@user_passes_test(lambda u: u.is_superuser or u.role in ['admin', 'staff'])
def create_suggestion(request):
        if request.method == 'POST':
            gram_panchayat_id = request.POST.get('gram_panchayat')
            work_type_id = request.POST.get('work_type')
            
            # Validate input data
            if not all([gram_panchayat_id, work_type_id]):
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)
            
            try:
                gram_panchayat = GramPanchayat.objects.get(id=gram_panchayat_id)
                work_type = WorkType.objects.get(id=work_type_id)
                
                # Create new suggestion
                suggestion = WorkSuggestion.objects.create(
                    gram_panchayat=gram_panchayat,
                    work_type=work_type,
                    created_by=request.user
                )
                
                # Log activity
                log_user_activity(
                    user=request.user,
                    activity_type="Work Suggestion Addition",
                    description=f"Work suggestion for '{work_type.name_en}' added for {gram_panchayat.name}",
                    created_by=request.user
                )
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Work suggestion created successfully',
                    'suggestion_id': suggestion.id
                })
                
            except (GramPanchayat.DoesNotExist, WorkType.DoesNotExist) as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
@user_passes_test(lambda u: u.is_superuser or u.role in ['admin', 'staff'])
def edit_suggestion(request, suggestion_id):
        suggestion = get_object_or_404(WorkSuggestion, id=suggestion_id)
        
        if request.method == 'GET':
            # Return the suggestion details for editing
            return render(request, 'edit_suggestion.html', {
                'suggestion': suggestion,
                'districts': District.objects.all(),
                'talukas': Taluka.objects.filter(district=suggestion.gram_panchayat.taluka.district),
                'grams': GramPanchayat.objects.filter(taluka=suggestion.gram_panchayat.taluka),
                'sectors': WorkType.objects.values_list('sector', flat=True).distinct().exclude(sector__isnull=True),
                'work_types': WorkType.objects.filter(sector=suggestion.work_type.sector)
            })
        
        elif request.method == 'POST':
            gram_panchayat_id = request.POST.get('gram_panchayat')
            work_type_id = request.POST.get('work_type')
            
            # Validate input data
            if not all([gram_panchayat_id, work_type_id]):
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)
            
            try:
                gram_panchayat = GramPanchayat.objects.get(id=gram_panchayat_id)
                work_type = WorkType.objects.get(id=work_type_id)
                
                # Update suggestion
                suggestion.gram_panchayat = gram_panchayat
                suggestion.work_type = work_type
                suggestion.save()
                
                # Log activity
                log_user_activity(
                    user=request.user,
                    activity_type="Work Suggestion Update",
                    description=f"Work suggestion for '{work_type.name_en}' updated for {gram_panchayat.name}",
                    created_by=request.user
                )
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Work suggestion updated successfully'
                })
                
            except (GramPanchayat.DoesNotExist, WorkType.DoesNotExist) as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
@user_passes_test(lambda u: u.is_superuser or u.role in ['admin', 'staff'])
def delete_suggestion(request, suggestion_id):
        suggestion = get_object_or_404(WorkSuggestion, id=suggestion_id)
        
        # Allow DELETE method or POST method with delete action
        if request.method == 'DELETE' or (request.method == 'POST' and request.POST.get('action') == 'delete'):
            work_type_name = suggestion.work_type.name_en
            gram_name = suggestion.gram_panchayat.name
            
            # Delete suggestion
            suggestion.delete()
            
            # Log activity
            log_user_activity(
                user=request.user,
                activity_type="Work Suggestion Deletion",
                description=f"Work suggestion for '{work_type_name}' deleted for {gram_name}",
                created_by=request.user
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Work suggestion deleted successfully'
            })
        
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def get_work_types(request):
        sector = request.GET.get('sector')
        if not sector:
            return JsonResponse([], safe=False)
        
        work_types = WorkType.objects.filter(sector=sector).values('id', 'name_en', 'name_mr')
        return JsonResponse(list(work_types), safe=False)