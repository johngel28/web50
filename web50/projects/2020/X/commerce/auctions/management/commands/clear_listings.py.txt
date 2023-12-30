# auctions/management/commands/clear_listings.py
from django.core.management.base import BaseCommand
from auctions.models import Listing

class Command(BaseCommand):
    help = 'Clears all listings from the database'

    def handle(self, *args, **kwargs):
        Listing.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all listings'))
