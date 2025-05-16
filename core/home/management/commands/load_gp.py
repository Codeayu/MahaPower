import os
import pandas as pd
from django.core.management.base import BaseCommand
from home.models import GramPanchayat, Taluka

class Command(BaseCommand):
    help = "Load Gram Panchayat data from CSV files with English and Marathi names"

    def handle(self, *args, **kwargs):
        # Corrected mapping
        taluka_mapping = {
            "achalpur": 1,
            "amravati": 2,
            "anjangaon-s": 3,  # ✅ Fixed spelling here
            "bhatkuli": 4,
            "chandur-bz": 5,
            "chandur-ril": 6,
            "chikhaldara": 7,
            "daryapur": 8,
            "dhamangaon-ril": 9,
            "dharni": 10,
            "morshi": 11,
            "nandgaon-kh": 12,
            "tiwsa": 13,
            "warud": 14
        }

        data_folder = "home/ex"  # Update if needed

        try:
            for filename in os.listdir(data_folder):
                if filename.endswith(".csv") and filename.startswith("gram_panchayats_"):
                    file_path = os.path.join(data_folder, filename)
                    taluka_key = filename.replace("gram_panchayats_", "").replace(".csv", "").lower()

                    taluka_id = taluka_mapping.get(taluka_key)
                    if not taluka_id:
                        self.stderr.write(self.style.ERROR(f"Taluka key '{taluka_key}' not found in mapping. Skipping file {filename}."))
                        continue

                    try:
                        taluka = Taluka.objects.get(id=taluka_id)
                    except Taluka.DoesNotExist:
                        self.stderr.write(self.style.ERROR(f"Taluka ID {taluka_id} does not exist in DB. Skipping {filename}."))
                        continue

                    df = pd.read_csv(file_path)
                    for _, row in df.iterrows():
                        name_en = str(row["name_en"]).strip()
                        name_mr = str(row["name_mr"]).strip()

                        GramPanchayat.objects.create(
                            name_en=name_en,
                            name_mr=name_mr,
                            taluka=taluka
                        )
                        self.stdout.write(self.style.SUCCESS(f"✅ Added GP: {name_en} -> {name_mr} in {taluka.name_en}"))

            self.stdout.write(self.style.SUCCESS("🎉 All Gram Panchayats inserted successfully."))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Error: {str(e)}"))
            self.stderr.write(self.style.ERROR("Failed to load Gram Panchayats."))
