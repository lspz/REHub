from django.core.management.base import BaseCommand, CommandError
from rescrap import models

class Command(BaseCommand):

  def handle(self, *args, **options):
    # huh? makes all lowercase
    self.clean_suburb()
    self.clean_agency()

  def clean_suburb(self):
    prefix = '[suburb] - '
    print prefix + 'Cleaning up suburbs..'
    rename_count = 0
    del_count = 0
    
    suburbs = models.Suburb.objects.all()
    for suburb_from in suburbs:
      name = suburb_from.name.lower().strip()
      suburbs_to = models.Suburb.objects.filter(name=name).exclude(id=suburb_from.id)
      
      if suburbs_to.count() == 0:
        suburb_from.name = name
        suburb_from.save()
        rename_count += 1
        print prefix + 'renaming to ' + name

      for suburb_to in suburbs_to:
        print prefix + 'from: "' + suburb_from.name + '" to: "' + suburb_to.name + '"'
        addresses = models.Address.objects.filter(suburb = suburb_from)
        print prefix + 'changed ' + str(len(addresses)) + ' addresses'
        for addr in addresses:
          addr.suburb = suburb_to
          addr.save()
        print prefix + 'deleting "' + suburb_from.name + '"'
        suburb_from.delete()
        del_count += 1
    print prefix + 'Total rename: ' + str(rename_count)
    print prefix + 'Total deletion: ' + str(del_count)

  def clean_agency(self):
    prefix = '[agency] - '
    print prefix + 'Cleaning up suburbs..'
    del_count = 0
    agencies = models.Agency.objects.all()
    for agency_from in agencies:
      name = agency_from.name.lower().strip()
      agencies_to = models.Agency.objects.filter(name=name).exclude(id=agency_from.id)
      for agency_to in agencies_to:
        print prefix + 'from: "' + agency_from.name + '" to: "' + agency_to.name + '"'
        listings = models.Listing.objects.filter(agency = agency_from)
        print prefix + 'changed ' + str(len(listings)) + ' listings'
        for listing in listings:
          listing.agency = agency_to
          listing.save()
        print prefix + 'deleting "' + agency_from.name + '"'
        agency_from.delete()
        del_count += 1
    print prefix + 'Total deletion: ' + str(del_count)