from django.core.management.base import BaseCommand
from home.models import WorkType, WorkSuggestion, GramPanchayat, Sector
import pandas as pd
import os

class Command(BaseCommand):
    help = "📊 Create WorkTypes from Excel and assign to all Gram Panchayats"

    def handle(self, *args, **kwargs):
        # === Step 1: Load Excel ===
        excel_path = "home/ex/aka.xlsx"  # Adjust path if needed
        self.stdout.write("📥 Reading Excel file...")

        try:
            df = pd.read_excel(excel_path)  # Columns: name_en, name_mr, sector
            df.dropna(subset=["name_en", "name_mr", "sector"], inplace=True)  # Clean data
        except Exception as e:
            self.stderr.write(f"❌ Error reading Excel file: {e}")
            return

        # === Step 2: Get sectors by ID ===
        self.stdout.write("🔍 Loading Sector objects...")
        
        try:
            df['sector'] = df['sector'].astype(int)
        except:
            self.stderr.write("⚠️ Warning: Could not convert sector values to integers")

        sector_ids = df['sector'].unique()
        sectors = {sector.id: sector for sector in Sector.objects.filter(id__in=sector_ids)}
        
        # Check if all sector IDs exist in database
        missing_sectors = set(sector_ids) - set(sectors.keys())
        if missing_sectors:
            self.stderr.write(f"❌ Some sectors not found in database: {missing_sectors}")
            return

        # === Step 3: Create WorkType entries ===
        self.stdout.write("⚙️ Creating WorkType entries...")

        worktype_objs = []
        for _, row in df.iterrows():
            sector_id = row["sector"]
            worktype_objs.append(
                WorkType(
                    name_en=row["name_en"].strip(),
                    name_mr=row["name_mr"].strip(),
                    sector=sectors[sector_id]  # Use Sector object instead of string
                )
            )

        WorkType.objects.bulk_create(worktype_objs)
        self.stdout.write(self.style.SUCCESS(f"✅ {len(worktype_objs)} WorkTypes created."))

        # === Step 4: Assign WorkSuggestions to all Gram Panchayats ===
        self.stdout.write("📌 Assigning WorkTypes to all Gram Panchayats...")

        gps = GramPanchayat.objects.all()
        all_worktypes = WorkType.objects.all()
        suggestion_objs = []

        for gp in gps:
            for work in all_worktypes:
                suggestion_objs.append(WorkSuggestion(gram_panchayat=gp, work_type=work))

        WorkSuggestion.objects.bulk_create(suggestion_objs)
        self.stdout.write(self.style.SUCCESS(
            f"🎯 {len(suggestion_objs)} WorkSuggestions assigned to {gps.count()} Gram Panchayats."
        ))

        self.stdout.write(self.style.SUCCESS("🏁 Process completed successfully."))
