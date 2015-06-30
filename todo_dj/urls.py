from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api

from items.resources import ItemResource, UserResource

api = Api(api_name='v1')
api.register(ItemResource())
api.register(UserResource())

#item_resource = ItemResource()

urlpatterns = patterns('',
    #url(r'^todo/', include(item_resource.urls)),
    url(r'^api/', include(api.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
