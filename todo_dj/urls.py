from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api

from items.resources import ItemResource, UserResource, LoginResource

api = Api(api_name='v1')
api.register(ItemResource())
api.register(UserResource())
api.register(LoginResource())

urlpatterns = patterns('',
    url(r'^api/', include(api.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
