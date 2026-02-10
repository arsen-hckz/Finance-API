from django.core.management.base import BaseCommand
from API.models import Category

class Command(BaseCommand):
    help = 'Populates category with some Greek finance categories'

    def handle(self,*args,**kwargs):
        # Category list: (Name, is_income)
        categories = [
            ('Μισθος',True),
            ('Supermarket',False),
            ('Επένδυση',False),
            ('Ρουχισμός',False),
            ('Βενζίνες/Μεταφορικα',False),
            ('Θέρμανση',False),
            ('Ενοίκιο',False),
            ('Ενεργεια',False),
            ('Έξοδοι/Εστιάση',False),
        ]

        self.stdout.write('Starting category seed...')

        for name,income_status in categories:
            obj,created = Category.objects.get_or_create(
                name = name,
                defaults={'is_income': income_status},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created:{name}"))
            else :
                self.stdout.write(f'Skipped:{name},(already exists)')

                
        self.stdout.write(self.style.SUCCESS('Seeding complete!'))