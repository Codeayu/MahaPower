from django.core.management.base import BaseCommand
from home.models import WorkType, WorkSuggestion, GramPanchayat, Taluka, Sector
from django.db import transaction

class Command(BaseCommand):
    help = "🎯 Assign a specific work suggestion to all Gram Panchayats under a taluka and mark as specialty"

    def add_arguments(self, parser):
        parser.add_argument('taluka_id', type=int, help='ID of the taluka')
        parser.add_argument('work_type_id', type=int, help='ID of the work type to assign')
        parser.add_argument('--specialty', action='store_true', help='Mark this work suggestion as specialty (default: True)')

    def handle(self, *args, **kwargs):
        taluka_id = kwargs['taluka_id']
        work_type_id = kwargs['work_type_id']
        is_specialty = kwargs.get('specialty', True)  # Default to True for specialty

        # === Step 1: Validate Taluka ===
        try:
            taluka = Taluka.objects.get(id=taluka_id)
            self.stdout.write(f"🏛️ Selected Taluka: {taluka.name_en} ({taluka.name_mr})")
        except Taluka.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"❌ Taluka with ID {taluka_id} does not exist"))
            return

        # === Step 2: Validate WorkType ===
        try:
            work_type = WorkType.objects.get(id=work_type_id)
            self.stdout.write(f"⚙️ Selected Work Type: {work_type.name_en} ({work_type.name_mr})")
            self.stdout.write(f"🏭 Sector: {work_type.sector.name_en} ({work_type.sector.name_mr})")
        except WorkType.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"❌ WorkType with ID {work_type_id} does not exist"))
            return

        # === Step 3: Get all Gram Panchayats under this Taluka ===
        gram_panchayats = GramPanchayat.objects.filter(taluka=taluka)
        
        if not gram_panchayats.exists():
            self.stderr.write(self.style.ERROR(f"❌ No Gram Panchayats found under taluka {taluka.name_en}"))
            return

        self.stdout.write(f"📍 Found {gram_panchayats.count()} Gram Panchayats under {taluka.name_en}")

        # === Step 4: Check for existing suggestions ===
        existing_suggestions = WorkSuggestion.objects.filter(
            gram_panchayat__taluka=taluka,
            work_type=work_type
        )
        
        if existing_suggestions.exists():
            self.stdout.write(self.style.WARNING(
                f"⚠️ {existing_suggestions.count()} existing suggestions found. They will be updated."
            ))
            
            # Update existing suggestions
            with transaction.atomic():
                existing_suggestions.update(is_specialty=is_specialty)
            
            self.stdout.write(self.style.SUCCESS(
                f"✅ Updated {existing_suggestions.count()} existing suggestions"
            ))

        # === Step 5: Create new suggestions for GPs that don't have this work type ===
        existing_gp_ids = set(existing_suggestions.values_list('gram_panchayat_id', flat=True))
        new_suggestions = []

        for gp in gram_panchayats:
            if gp.id not in existing_gp_ids:
                new_suggestions.append(
                    WorkSuggestion(
                        gram_panchayat=gp,
                        work_type=work_type,
                        is_specialty=is_specialty
                    )
                )

        if new_suggestions:
            with transaction.atomic():
                WorkSuggestion.objects.bulk_create(new_suggestions)
            
            self.stdout.write(self.style.SUCCESS(
                f"✅ Created {len(new_suggestions)} new work suggestions"
            ))

        # === Step 6: Summary ===
        specialty_text = "as SPECIALTY" if is_specialty else "as REGULAR"
        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎯 SUMMARY:\n"
                f"   Taluka: {taluka.name_en} ({taluka.name_mr})\n"
                f"   Work Type: {work_type.name_en} ({work_type.name_mr})\n"
                f"   Sector: {work_type.sector.name_en}\n"
                f"   Total GPs affected: {gram_panchayats.count()}\n"
                f"   Marked {specialty_text}\n"
                f"   ✅ Process completed successfully!"
            )
        )

        # === Step 7: Display affected Gram Panchayats ===
        self.stdout.write("\n📋 Affected Gram Panchayats:")
        for gp in gram_panchayats[:10]:  # Show first 10
            self.stdout.write(f"   • {gp.name_en} ({gp.name_mr})")
        
        if gram_panchayats.count() > 10:
            self.stdout.write(f"   ... and {gram_panchayats.count() - 10} more")
