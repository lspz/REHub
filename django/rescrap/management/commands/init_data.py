from django.core.management.base import BaseCommand, CommandError
from rescrap import models

class Command(BaseCommand):

  def handle(self, *args, **options):
    print 'Creating initial data...'
    models.FeedSource.objects.get_or_create(name='realestate.com.au', base_url='realestate.com.au', img_path='realestate.png')
    models.FeedSource.objects.get_or_create(name='domain.com.au', base_url='domain.com.au', img_path='domain.png')
    models.FeedSource.objects.get_or_create(name='harcourts', base_url='harcourts.com.au')