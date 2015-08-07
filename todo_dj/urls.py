from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from items.resources import ItemResource, UserResource, LoginResource, RegistrationResource
from items.resources import GroupResource, ExportResource

api = Api(api_name='v1')
api.register(ItemResource())
api.register(UserResource())
api.register(LoginResource())
api.register(RegistrationResource())
api.register(GroupResource())
api.register(ExportResource())

urlpatterns = patterns('',
    url(r'^api/', include(api.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
