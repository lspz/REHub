from django.db import models

class PriceType:
  FIXED = 'F'
  NEGOTIABLE = 'N'
  AUCTION = 'A'

class PropertyType:
  HOUSE = 'H'
  APARTMENT = 'A'
  UNIT = 'U'
  TOWNHOUSE = 'T'

# Ensure this match the one in fixtures/init command
class FeedSourceEnum:
  RECOMAU= 1
  DOMAIN=2
  HARCOURTS=3

class ImportBatch(models.Model):
  date = models.DateTimeField(auto_now_add=True)

class Suburb(models.Model):
  name = models.CharField(max_length=300, db_index=True, blank=True)
  state = models.CharField(max_length=3, db_index=True, blank=True)
  postcode = models.CharField(max_length=4, db_index=True, blank=True)

class AddressManager(models.Manager):
  def get_or_create_address(self, raw='', address='', suburb='', state='', postcode='', loc_lat=None, loc_long=None):
    address = address.lower().strip()
    if address != '':
      res = self.filter(address=address)
      if res.count() > 0:
        return res[0]
    elif raw != '':
      res = self.filter(raw=raw)
      if res.count() > 0:
        return res[0]     
    else:
      return None
    new_address = self.model(raw=raw, address=address, loc_lat=loc_lat, loc_long=loc_long)
    if suburb != '':
      new_address.suburb, created = Suburb.objects.get_or_create(name=suburb.lower().strip())
      if created:
        # huh? some sites doesn't list these at front
        new_address.suburb.state = state.lower().strip()
        new_address.suburb.postcode = postcode.lower().strip()

    new_address.save()
    return new_address

class Address(models.Model):
  objects = AddressManager()
  raw = models.CharField(max_length=300, blank=True)
  address = models.CharField(max_length=300, db_index=True, blank=True)
  suburb = models.ForeignKey(Suburb, blank=True, null=True)
  loc_lat = models.FloatField(blank=True, null=True)
  loc_long = models.FloatField(blank=True, null=True)

class FeedSource(models.Model):
  name = models.CharField(max_length=50)
  base_url = models.CharField(max_length=100)
  img_path = models.CharField(max_length=50, blank=True, default='')

class Agency(models.Model):
  name = models.CharField(max_length=30, db_index=True)
  img_path = models.CharField(max_length=50, blank=True, default='')

class ListingManager(models.Manager):
  def has_duplicate(self, listing):
    # This is scrapy listing item, not django
    return self.filter(source=listing['source'], address=listing['address']).exists()

class Listing(models.Model):
  objects = ListingManager()

  PRICE_TYPE_CHOICES = (
    (PriceType.FIXED, 'Fixed'),
    (PriceType.NEGOTIABLE, 'Negotiable'),
    (PriceType.AUCTION, 'Auction')
  )

  address = models.ForeignKey(Address, blank=True, null=True)
  source = models.ForeignKey(FeedSource, blank=True, null=True)
  agency = models.ForeignKey(Agency, blank=True, null=True) 
  batch = models.ForeignKey(ImportBatch)
  url = models.CharField(max_length=200, blank=True)
  img_path = models.CharField(max_length=50, blank=True)
  property_type_raw = models.CharField(max_length=30, blank=True)
  #property_type = models.CharField(max_length=1, blank=True)
  bedrooms = models.IntegerField(blank=True, null=True)
  bathrooms = models.IntegerField(blank=True, null=True)
  carparks = models.IntegerField(blank=True, null=True)
  title_desc = models.CharField(max_length=100, blank=True)
  short_desc = models.CharField(max_length=300, blank=True)
  price_raw = models.CharField(max_length=50, blank=True)
  price_min = models.FloatField(blank=True, null=True)
  price_high = models.FloatField(blank=True, null=True)
  price_type = models.CharField(max_length=1, choices=PRICE_TYPE_CHOICES, blank=True)
  pub_date = models.DateTimeField(blank=True, null=True)
  sysversion = models.DateTimeField(auto_now_add=True)

  def get_url_abs(self):
    return 'http://' + self.source.base_url + self.url

  # huh? implement
  def parse_raw_data(self):
    pass

  url_abs = property(get_url_abs)
  
  # def save(self):
  #   if (self.address != None) and (self.address.pk == None):
  #     self.address.save()
  #   if (self.agent != None) and (self.agent.pk == None):
  #     self.agent.save()
  #   super(Listing, self).save()

# huh? implement
# class ListingDetail(model.Models)
#   listing = models.ForeignKey(Listing, primary_key=True)
#   desc = models.CharField(max_length=3000, blank=True)
