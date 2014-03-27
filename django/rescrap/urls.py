from django.conf.urls import patterns, include, url
from rescrap import views, api

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
  url(r'^$', views.home, name='home'),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^api/', include('rescrap.api.urls')),
  url(r'^grappelli/', include('grappelli.urls')),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
