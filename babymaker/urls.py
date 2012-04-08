from django.conf.urls.defaults import *

urlpatterns = patterns('babymaker.views',
  url(r'^links/$', 'links', name='my_links'),
  url(r'^clusters/$', 'view_clusters', name='clusters'),
  url(r'^load_bookmarks/$', 'load_bookmarks', name='load_bookmarks'),
)