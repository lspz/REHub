from django.conf.urls import patterns, url
from rescrap.api.views import *

urlpatterns = patterns('',
  url(r'^suburbs/$', SuburbsAPIView.as_view()),
  url(r'^listings/(?P<suburb_ids>[\d-]+)/$', ListingsAPIView.as_view()),
)
