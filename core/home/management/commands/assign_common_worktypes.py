from django.core.management.base import BaseCommand
from home.models import WorkType, WorkSuggestion, GramPanchayat

COMMON_WORKS_SECTORWISE = {
    "Dairy Business": "Agriculture/Food",
    "Dry Fruit Shop": "Agriculture/Food",
    "Goat Farming": "Agriculture/Food",
    "Poultry Farming": "Agriculture/Food",
    
    "Spice Making Unit": "Agriculture/Food",
    "Papad and Pickle Production": "Agriculture/Food",
    "Bakery Products": "Agriculture/Food",
    "Potato/Banana Wafers": "Agriculture/Food",
    "Fruit Jam / Jelly / Murabba": "Agriculture/Food",
    "Poha / Daliya Production": "Agriculture/Food",

    "Agarbatti Making": "Polymer/Chemical",
    "Soap & Detergent Production": "Polymer/Chemical",
    "Candle Manufacturing": "Polymer/Chemical",
    "Plastic Bag Making": "Polymer/Chemical",
    "Plastic Bottle Making": "Polymer/Chemical",
    "Idol Making": "Polymer/Chemical",

    "Cement Block / Brick Unit": "Mineral-Based",
    "Marble / Stone Polishing": "Mineral-Based",

    "Banana Leaf / Areca Plate Making": "Paper & Fiber",
    "Handmade Paper Cups / Plates": "Paper & Fiber",

    "Cycle Repair & Plumbing": "Engineering & Tools",
    "Auto Service Station": "Engineering & Tools",
    "Basic Electronics Repair": "Engineering & Tools",

    "Tailoring & Garment Stitching": "Textile/Services",
    "Laundry / Ironing Service": "Textile/Services",
    "Embroidery Work": "Textile/Services",
    "Screen Printing": "Textile/Services",
    "Xerox & Printing": "Textile/Services",
    "Mobile Repairing": "Engineering & Tools",
    "Electrical Repairing": "Engineering & Tools",
    "Computer Repairing": "Engineering & Tools",
    "Carpentry": "Engineering & Tools",
    "Tailoring": "Textile/Services",
    "furniture making": "Engineering & Tools",
    "Sewing Machine Repair": "Engineering & Tools",
    "Embroidery": "Textile/Services",
    "Vehicle Repairing": "Engineering & Tools",
    "Welding": "Engineering & Tools",
    "Blacksmith": "Engineering & Tools",
    "Plumbing": "Engineering & Tools",
    "Laundry": "Textile/Services",
    "Catering": "Textile/Services",
    "Beauty Parlour / Face Cream": "Textile/Services",
    "PhotoStudio": "Textile/Services",
}

class Command(BaseCommand):
    help = "Create sector-wise work types and assign to every Gram Panchayat"

    def handle(self, *args, **kwargs):
        self.stdout.write("🔁 Creating sector-wise work types...")

        created_count = 0
        work_objs = []

        for name, sector in COMMON_WORKS_SECTORWISE.items():
            obj, created = WorkType.objects.get_or_create(
                name_en=name,
                defaults={"sector": sector}
            )
            work_objs.append(obj)
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {created_count} new WorkTypes created."))

        gps = GramPanchayat.objects.all()
        total_suggestions = 0

        self.stdout.write("🗂 Assigning all work types to every Gram Panchayat...")

        for gp in gps:
            for work in work_objs:
                _, new = WorkSuggestion.objects.get_or_create(
                    gram_panchayat=gp,
                    work_type=work
                )
                if new:
                    total_suggestions += 1

        self.stdout.write(self.style.SUCCESS(
            f"🎯 Successfully assigned {total_suggestions} suggestions to {gps.count()} GPs."
        ))
