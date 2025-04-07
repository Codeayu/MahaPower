from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Scheme
from django.contrib import messages

def index(request):
    schemes = Scheme.objects.all()

    scheme_type = request.GET.get('type')
    sector = request.GET.get('sector')
    lang = request.GET.get('lang', 'en')

    if scheme_type:
        schemes = schemes.filter(scheme_type=scheme_type)
    if sector:
        schemes = schemes.filter(sector=sector)

    return render(request, 'index.html', {
        'schemes': schemes,
        'lang': lang,
    })

def scheme_detail(request, scheme_id):
    scheme = get_object_or_404(Scheme, id=scheme_id)
    lang = request.GET.get('lang', 'en')
    return render(request, 'scheme_detail.html', {'scheme': scheme, 'lang': lang})

def is_admin(user):
    return user.is_superuser

def is_staff_user(user):
    return user.is_authenticated and user.is_staff_user

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff_user)
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
        website_link = request.POST.get('website_link')

        if not all([name_en, name_mr, scheme_type, sector, summary_en]):
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
                website_link=website_link,
                created_by=request.user
            )
            messages.success(request, "Scheme added successfully!")
            return redirect('index')

    return render(request, 'add_scheme.html')
