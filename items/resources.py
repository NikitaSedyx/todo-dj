from tastypie.resources import ModelResource, Resource
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication

from django.contrib.sessions.models import Session

from  django.conf.urls import url
from django.contrib import auth
from django.http import HttpResponse

from items.models import Item
from django.contrib.auth.models import User

import json

class UserAuthorization(Authorization):

  def get_user(self, bundle):
    return bundle.request.user

  def read_list(self, object_list, bundle):
    return object_list.filter(user=self.get_user(bundle))

  def read_detail(self, object_list, bundle):
    return bundle.obj.user == bundle.request.user

  def update_detail(self, object_list, bundle):
    return bundle.obj.user == bundle.request.user

  def create_detail(self, object_list, bundle):
    bundle.obj.user = self.get_user(bundle)
    return True

  def delete_detail(self, object_list, bundle):
    return bundle.obj.user == bundle.request.user



class UserResource(ModelResource):
  class Meta:
    queryset = User.objects.all()
    resource_name = 'user'
    excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']



class ItemResource(ModelResource):
  user = fields.ForeignKey(UserResource, 'user')
  class Meta:
    queryset = Item.objects.all()
    resource_name = 'item'
    authentication = SessionAuthentication()
    authorization= UserAuthorization()
    allowed_methods = ['get', 'post', 'put', 'delete']

class LoginResource(Resource):
  class Meta:
    resource_name = 'auth'

  def prepend_urls(self):
    return [
      url(r'^%s/login/$' % self._meta.resource_name, self.wrap_view('login'), name='api_login'),
      url(r'^%s/logout/$' % self._meta.resource_name, self.wrap_view('logout'), name='api_logout'),
      url(r'^%s/info/$' % self._meta.resource_name, self.wrap_view('get_user'), name='api_get_info'),
    ]

  def login(self, request, **kwargs):
    if request.method == 'POST':
      data = json.loads(request.body)
      username = data['username']
      password = data['password']
      user = auth.authenticate(username=username, password=password)
      if user is not None:
        auth.login(request, user)
        return HttpResponse(user)
      else:
        return HttpResponse(status=500)
    else:
      return HttpResponse(status=500)

  def logout(self, request, **kwargs):
    auth.logout(request)
    return HttpResponse(status=200)

  def get_user(self, request, **kwargs):
    return HttpResponse(request.user)


