from scrapy.contrib.djangoitem import DjangoItem
from rescrap.models import Listing

class ListingItem(DjangoItem):
  django_model = Listing