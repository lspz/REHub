from django.core.management.base import BaseCommand, CommandError
from rescrap import models

class Command(BaseCommand):

  def handle(self, *args, **options):
    print 'Creating initial data...'
    models.FeedSource.objects.get_or_create(name='realestate.com.au', base_url='realestate.com.au')
    models.FeedSource.objects.get_or_create(name='domain.com.au', base_url='domain.com.au')
    models.FeedSource.objects.get_or_create(name='harcourts', base_url='harcourts.com.au')