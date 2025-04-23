import pandas as pd
from django.core.management.base import BaseCommand
from home.models import District, Taluka, GramPanchayat
from django.db import connection

class Command(BaseCommand):
    help = "Import Gram Panchayat data from Excel file"

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help='Path to Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['filepath']
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to read Excel file: {e}"))
            return

        created = 0
        for index, row in df.iterrows():
            try:
                district_name = row['District Name'].strip()
                taluka_name = row['Block Name'].strip()
                gp_name = row['Gram Panchayat Name'].strip()

                district, _ = District.objects.get_or_create(name=district_name)
                taluka, _ = Taluka.objects.get_or_create(name=taluka_name, district=district)
                gp, created_gp = GramPanchayat.objects.get_or_create(name=gp_name, taluka=taluka)

                if created_gp:
                    created += 1

                # close DB connection every 50 records to avoid timeout
                if index % 50 == 0:
                    connection.close()

            except Exception as e:
                self.stderr.write(self.style.WARNING(f"Error at row {index}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Imported successfully. GPs created: {created}"))
