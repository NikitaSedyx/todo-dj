from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication

from items.models import Item
from django.contrib.auth.models import User

class UserResource(ModelResource):
  class Meta:
    queryset = User.objects.all()
    resource_name = 'user'
    excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
    allowed_methods = ['get']



class ItemResource(ModelResource):
  user = fields.ForeignKey(UserResource, 'user')
  class Meta:
    queryset = Item.objects.all()
    resource_name = 'item'
    #authorization= Authorization()
    authentication = SessionAuthentication()
    #authorization = DjangoAuthorization()
    list_allowed_methods = ['get', 'post']
