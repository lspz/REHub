from django.db.models import Q
from rest_framework import viewsets, routers, serializers, generics
from rescrap.models import Suburb, Address, Listing

class SuburbSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Suburb
    fields = ('id', 'name')
    
class SuburbsAPIView(generics.ListAPIView):
  queryset = Suburb.objects.all()
  serializer_class = SuburbSerializer

class ListingSerializer(serializers.ModelSerializer):
  address = serializers.SlugRelatedField(many=False, read_only=True, slug_field='address')
  source = serializers.SlugRelatedField(many=False, read_only=True, slug_field='img_path')
  url = serializers.Field(source='url_abs') 
  
  class Meta:
    model = Listing
    many = True
    fields = (
      'id', 
      'address', 
      'url', 
      'img_path', 
      'price_raw', 
      'title_desc', 
      'short_desc',
      'source',
      'bedrooms',
      'bathrooms',
      'carparks'
    )


# huh? group by address so there's no duplicate. Need new UniqueListing model
class ListingsAPIView(generics.ListAPIView):
  serializer_class = ListingSerializer

  LISTING_PER_PAGE = 10

  # Limit 20 for now
  def get_queryset(self):
    suburb_ids = self.kwargs['suburb_ids'].split('-')
    page_no = int(self.kwargs['page_no'])
    look_from = page_no * self.LISTING_PER_PAGE
    look_to = look_from + self.LISTING_PER_PAGE - 1
    # huh? get all suburbs
    # print self.request.GET.get('a')
    return Listing.objects.filter(address__suburb__id=suburb_ids[0])[look_from:look_to]
