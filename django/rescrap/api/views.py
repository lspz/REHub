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
      'bedrooms',
      'bathrooms',
      'carparks'
    )


# huh? group by address so there's no duplicate. Need new UniqueListing model
class ListingsAPIView(generics.ListAPIView):
  serializer_class = ListingSerializer

  # Limit 20 for now
  def get_queryset(self):
    # huh? get all
    suburb_ids = self.kwargs['suburb_ids'].split('-')
    return Listing.objects.filter(address__suburb__id=suburb_ids[0])[:20]
