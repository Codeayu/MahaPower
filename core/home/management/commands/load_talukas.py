from django.core.management.base import BaseCommand
from home.models import Taluka, District

class Command(BaseCommand):
    help = 'Load talukas into the database for District ID 4 (Amravati)'

    def handle(self, *args, **kwargs):
        try:
            district = District.objects.get(id=1)
        except District.DoesNotExist:
            self.stdout.write(self.style.ERROR('District with id=4 does not exist. Please create it first.'))
            return

        talukas = [
    ('Achalpur', 'अचलपूर'),
    ('Amravati', 'अमरावती'),
    ('Anjangaon Surji', 'अंजनगाव सुर्जी'),
    ('Bhatkuli', 'भातकुली'),
    ('Chandur Bazar', 'चांदूर बाजार'),
    ('Chandur Railway', 'चांदूर रेल्वे'),
    ('Chikhaldara', 'चिखलदरा'),
    ('Daryapur', 'दर्यापूर'),
    ('Dhamangaon Railway', 'धामणगाव रेल्वे'),
    ('Dharni', 'धारणी'),
    ('Morshi', 'मोर्शी'),
    ('Nandgaon Khandeshwar', 'नांदगाव खंडेश्वर'),
    ('Tivsa', 'तिवसा'),
    ('Warud', 'वरुड'),
]

        for name_en, name_mr in talukas:
            Taluka.objects.get_or_create(
                name_en=name_en,
                name_mr=name_mr,
                district=district
            )

        self.stdout.write(self.style.SUCCESS('Talukas for District ID 4 inserted successfully.'))
