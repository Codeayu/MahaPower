"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from home import views
from home.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('faqs/', views.faqs, name='faqs'),
    path('our_team/', views.team, name='our_team'),
    
    path('scheme/<int:scheme_id>/', scheme_detail, name='scheme_detail'),
    path('add-scheme/', add_scheme, name='add_scheme'),
    path('register/', register, name='register'),
    path('scheme_detail/<int:scheme_id>/', scheme_detail, name='scheme_detail'),
    path('login/', login_view, name='login'), 
    path('admin_user/', admin_user, name='admin_user'),
    path('logout/', logout_user, name='logout'),
    path('staff_user/', staff_user, name='staff_user'), 
    path('staff_user_approval/', staff_user_approval, name='staff_user_approval'),
    path('activate-user/<int:user_id>/', activate_user, name='activate_user'),  
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('manage_scheme/', manage_scheme, name='manage_scheme'),
    path('update_scheme/<int:scheme_id>/', update_scheme, name='update_scheme'),
    path('delete_scheme/<int:scheme_id>/', delete_scheme, name='delete_scheme'),
    path('scheme/<int:scheme_id>/history/', scheme_history_view, name='scheme_history'),
    path('send_test_email/', send_test_email, name='send_email'),
    
    path('user_profile_edit/', user_profile_edit, name='user_profile_edit'),
    path('password_reset_flow/', password_reset_flow, name='password_reset_flow'),

    
    #under contsruction pages
    path('under_construction/', views.under_construction, name='under_construction'),
    
    #work suggestion pages
    path('suggestions/', get_work_suggestions, name='get_work_suggestions'),
    # Add this to your urlpatterns list
    path('get-suggestions/', get_suggestions, name='get_suggestions'),
    path('get-talukas/', get_talukas, name='get_talukas'),
    path('get-gram-panchayats/', get_gram_panchayats, name='get_gram_panchayats'),
    path('get-work-types/', get_work_types, name='get_work_types'),
    
    #managing suggestions
    # Managing work suggestions
    path('manage_suggestions/', manage_suggestions, name='manage_suggestions'),
    path('create-suggestion/', create_suggestion, name='create_suggestion'),
    
    path('edit-suggestion/<int:suggestion_id>/', edit_suggestion, name='edit_suggestion'),
    path('delete-suggestion/<int:suggestion_id>/', delete_suggestion, name='delete_suggestion'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
