from tastypie.resources import ModelResource, Resource
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication
from tastypie.paginator import Paginator
from tastypie.http import HttpNotFound, HttpForbidden, HttpUnauthorized
from django.contrib.sessions.models import Session
from django.conf.urls import url
from django.contrib import auth
from django.http import HttpResponse, HttpResponseServerError
from items.models import Item, Group
from django.contrib.auth.models import User, UserManager
import json
import xlwt
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

class ItemAuthorization(Authorization):

  def get_user(self, bundle):
    return bundle.request.user

  def read_list(self, object_list, bundle):
    return object_list.none()

  def read_detail(self, object_list, bundle):
    return self.get_user(bundle) in bundle.obj.group.users.all()

  def update_detail(self, object_list, bundle):
    return self.get_user(bundle) in bundle.obj.group.users.all()

  def create_detail(self, object_list, bundle):
    return self.get_user(bundle) in bundle.obj.group.users.all()

  def delete_detail(self, object_list, bundle):
    return self.get_user(bundle) in bundle.obj.group.users.all()


class GroupAuthorization(Authorization):

  def get_user(self, bundle):
    return bundle.request.user

  def read_list(self, object_list, bundle):
    if self.get_user(bundle).is_active:
      allowed = []
      user = self.get_user(bundle)
      for obj in object_list:
        if user in obj.users.all():
          allowed.append(obj)
      return allowed
    return []

  def read_detail(self, object_list, bundle):
    return self.get_user(bundle) in bundle.obj.users.all()

  def update_detail(self, object_list, bundle):
    return self.get_user(bundle) in bundle.obj.users.all()

  def create_detail(self, object_list, bundle):
    bundle.obj.creator = self.get_user(bundle)
    return True

  def delete_detail(self, object_list, bundle):
    return bundle.request.user in bundle.obj.users.all()


class UserAuthorization(Authorization):

  def get_user(self, bundle):
    return bundle.request.user

  def read_list(self, object_list, bundle):
    if self.get_user(bundle).is_active:
      return object_list
    return []

  def read_detail(self, object_list, bundle):
    return self.get_user(bundle).is_active

  def create_detail(self, object_list, bundle):
    user = self.get_user(bundle)
    return user.is_superuser

  def update_detail(self, object_list, bundle):
    user = self.get_user(bundle)
    return bundle.obj == user or user.is_superuser

  def delete_detail(self, object_list, bundle):
    user = self.get_user(bundle)
    return bundle.obj == user or user.is_superuser


class UserResource(ModelResource):
  class Meta:
    queryset = User.objects.all()
    resource_name = 'user'
    excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
    authentication = SessionAuthentication()
    authorization = UserAuthorization()
    filtering = {
      'username': ('icontains', ),
    }


class GroupResource(ModelResource):
  creator = fields.ForeignKey(UserResource, 'creator', blank=True, full=True)
  users = fields.ManyToManyField(UserResource, 'users', blank=True, full=True)
  items = fields.ToManyField('items.resources.ItemResource', 'item_set', related_name="group", full=True)
  class Meta:
    queryset = Group.objects.filter(is_deleted=False)
    resource_name = 'group'
    authentication = SessionAuthentication()
    authorization = GroupAuthorization()
    paginator_class = Paginator
    limit = 10


class ItemResource(ModelResource):
  group = fields.ToOneField(GroupResource, 'group')
  class Meta:
    queryset = Item.objects.all()
    resource_name = 'item'
    authentication = SessionAuthentication()
    authorization = ItemAuthorization()
    paginator_class = Paginator
    limit = 10
    ordering = ['is_completed', 'description', 'deadline']
    filtering = {
      'description': ('icontains', ),
      'deadline': ('gt', ),
    }


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
    self.method_check(request, allowed=['post'])
    current_user = request.user
    if current_user.is_anonymous():
      data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
      username = data.get('username')
      password = data.get('password')
      user = auth.authenticate(username=username, password=password)
      if user is not None:
        if user.is_active:
          auth.login(request,user)
          return self.create_response(request, {'user': Unpacking.unpack_user(user)})
        else:
          return self.create_response(request, {}, HttpForbidden )
      else:
        return self.create_response(request, {}, HttpUnauthorized)
    else:
      return self.create_response(request, {'user': Unpacking.unpack_user(current_user)})

  def logout(self, request, **kwargs):
    self.method_check(request, allowed=['get'])
    if request.user and request.user.is_authenticated():
      auth.logout(request)
      return self.create_response(request, {})
    else:
      return self.create_response(request, {}, HttpUnauthorized)

  def get_user(self, request, **kwargs):
    user = request.user
    if user.is_anonymous():
      return self.create_response(request, {}, HttpUnauthorized)
    else:
      return self.create_response(request, Unpacking.unpack_user(user))


class RegistrationResource(Resource):
  class Meta:
    pass

  def prepend_urls(self):
    return [
      url(r'^registration/$', self.wrap_view('registration'), name='api_registration')
    ]

  def registration(self, request, **kwargs):
    self.method_check(request, allowed=['post'])
    data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
    username = data.get('username')
    password = data.get('password')
    repeatPassword = data.get('confirmPassword')
    try:
      user=User.objects.get(username=username)
      return self.create_response(request, {'success': False})
    except ObjectDoesNotExist:
      if password == repeatPassword:
        email = data.get('email')
        user = User.objects.create_user(username, email, password)
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        return self.create_response(request, {'success': True, 'user': Unpacking.unpack_user(user)})
      else:
        return self.create_response(request, {}, HttpUnauthorized)


class ExportResource(Resource):
  class Meta:
    resource_name = 'export'

  def prepend_urls(self):
    return [
      url(r'^%s/xls/(?P<id>\d+)/$' % self._meta.resource_name,
        self.wrap_view('export_xls'), name='api_export_xls')
    ]

  def export_xls(self, request, **kwargs):
    try:
      group = Group.objects.get(pk=kwargs['id'])
    except ObjectDoesNotExist:
      return self.create_response(request, {}, HttpNotFound)
    if request.user not in group.users.all():
      return self.create_response(request, {}, HttpForbidden)
    response = HttpResponse(content_type="application/xls")
    response['Content-Disposition'] = 'attachment; filename=file.xls'
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Page 1')
    line = 0
    sheet.write(line, 0, "name")
    sheet.write(line, 1, group.title)
    line += 1
    sheet.write(line, 0, "created at")
    sheet.write(line, 1, group.created_at.strftime('%d %b %Y'))
    line += 1
    sheet.write(line, 0, "updated at")
    sheet.write(line, 1, group.updated_at.strftime('%d %b %Y'))
    line += 1
    sheet.write(line, 0, "items:")
    line += 1
    sheet.write(line, 0, "description")
    sheet.write(line, 1, "Is completed")
    line += 1
    for item in group.item_set.all():
      sheet.write(line, 0, item.description)
      sheet.write(line, 1, str(item.is_completed))
      line += 1
    workbook.save(response)
    return response


class Unpacking:

  @staticmethod
  def unpack_user(user):
    return {
      'id': user.id,
      'username': user.username,
      'email': user.email,
      'first_name': user.first_name,
      'last_name': user.last_name,
      'last_login': user.last_login,
      'is_active': user.is_active,
    }
