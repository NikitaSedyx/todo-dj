from tastypie.test import ResourceTestCase
from .models import Item, Group
from django.contrib.auth.models import User
import json


class ItemResourceTest(ResourceTestCase):

  def setUp(self):
    super(ItemResourceTest, self).setUp()
    self.url = '/api/v1/item/'
    user_f = User.objects.create_user('user1', 'user1@mail.ru', 123)
    user_s = User.objects.create_user('user2', 'user2@mail.ru', 123)
    group = Group(title='test', creator=user_f)
    group.save()
    group.users.add(user_f)
    group.save()
    item = Item(description='test item 1', group=group)
    item.save()
    item = Item(description='test item 2', group=group)
    item.save()

  def setSession(self, username, password):
    return self.api_client.post('/api/v1/auth/login/', format='json', data={'username':username, 'password':password})

  def test_get_items_unauthorized(self):
    response = self.api_client.get(self.url, format='json')
    self.assertHttpUnauthorized(response)

  def test_create_item_unauthorized(self):
    response = self.api_client.post(self.url, format='json', data={})
    self.assertHttpUnauthorized(response)

  def test_put_item_unauthorized(self):
    url = self.url + '1/'
    response = self.api_client.put(url, format='json', data={})
    self.assertHttpUnauthorized(response)

  def test_delete_item_unauthorized(self):
    url = self.url + '1/'
    response = self.api_client.delete(url, format='json')
    self.assertHttpUnauthorized(response)

  def test_get_not_contributor(self):
    item = Item.objects.get(description='test item 1')
    url = self.url + str(item.pk) + '/'
    response = self.api_client.get(url, format='json',
      authentication=self.setSession('user2', 123))
    self.assertHttpUnauthorized(response)

  def test_put_not_contributor(self):
    item = Item.objects.get(description='test item 1')
    url = self.url + str(item.pk) + '/'
    response = self.api_client.put(url, format='json',
      data={}, authentication=self.setSession('user2', 123))
    self.assertHttpUnauthorized(response)

  def test_delete_not_contributor(self):
    item = Item.objects.get(description='test item 1')
    url = self.url + str(item.pk) + '/'
    response = self.api_client.delete(url, format='json',
      data={}, authentication=self.setSession('user2', 123))
    self.assertHttpUnauthorized(response)

  def test_get_items_authorized(self):
    response = self.api_client.get(self.url, format='json',
      authentication=self.setSession('user1', 123))
    self.assertValidJSONResponse(response)
    result = json.loads(response.content)['objects']
    self.assertEqual(len(result), 0)

  def test_create_item_authorized(self):
    group = Group.objects.all()[0]
    item = {
      'description': 'create test item',
      'group': '/api/v1/group/' + str(group.pk) + '/'
    }
    item_count = group.item_set.all().count()
    self.assertEqual(item_count, 2)
    response = self.api_client.post(self.url, format='json',
      authentication=self.setSession('user1', 123), data=item)
    self.assertHttpCreated(response)
    item_count = group.item_set.all().count()
    self.assertEqual(item_count, 3)

  def test_put_item_authorized(self):
    item = Item.objects.get(description='test item 1')
    url = self.url + str(item.pk) + '/'
    response = self.api_client.get(url, format='json',
      authentication=self.setSession('user1', 123))
    item = self.deserialize(response)
    item['is_completed'] = True
    response = self.api_client.put(url, format='json',
      authentication=self.setSession('user1', 123), data=item)
    self.assertHttpAccepted(response)
    item = Item.objects.get(description='test item 1')
    self.assertEqual(item.is_completed, True)

  def test_delete_item_authorized(self):
    group = Group.objects.all()[0]
    item_count = group.item_set.all().count()
    self.assertEqual(item_count, 2)
    item = Item.objects.get(description='test item 1')
    url = self.url + str(item.pk) + '/'
    response = self.api_client.delete(url, format='json',
      authentication=self.setSession('user1', 123))
    self.assertHttpAccepted(response)
    item_count = group.item_set.all().count()
    self.assertEqual(item_count, 1)


class GroupResourceTest(ResourceTestCase):

  def setUp(self):
    super(GroupResourceTest, self).setUp()
    self.url = '/api/v1/group/'
    user_f = User.objects.create_user('user1', 'user1@mail.ru', 123)
    user_s = User.objects.create_user('user2', 'user2@mail.ru', 123)
    group = Group(creator=user_f, title='test1')
    group.save()
    group.users.add(user_f)
    group.save()
    group = Group(creator=user_f, title='test2')
    group.save()
    group.users.add(user_f)
    group.users.add(user_s)
    group.save()

  def setSession(self, username, password):
    return self.api_client.post('/api/v1/auth/login/',
      format='json', data={'username':username, 'password':password})

  def test_get_groups_unauthorized(self):
    response = self.api_client.get(self.url, format='json')
    self.assertHttpUnauthorized(response)

  def test_create_group_unauthorized(self):
    response = self.api_client.post(self.url, format='json', data={})
    self.assertHttpUnauthorized(response)

  def test_put_item_unauthorized(self):
    url = self.url + '1/'
    response = self.api_client.put(url, format='json', data={})
    self.assertHttpUnauthorized(response)

  def test_delete_group_unauthorized(self):
    url = self.url + '1/'
    response = self.api_client.delete(url, format='json')
    self.assertHttpUnauthorized(response)

  def test_get_group_not_contibutor(self):
    group = Group.objects.get(title='test1')
    url = self.url + str(group.pk) + '/'
    response = self.api_client.get(url, format='json',
      authentication=self.setSession('user2', 123))
    self.assertHttpUnauthorized(response)

  def test_put_group_not_contibutor(self):
    group = Group.objects.get(title='test1')
    url = self.url + str(group.pk) + '/'
    response = self.api_client.put(url, format='json',
      authentication=self.setSession('user2', 123), data={})
    self.assertHttpUnauthorized(response)

  def test_delete_group_not_contibutor(self):
    group = Group.objects.get(title='test1')
    url = self.url + str(group.pk) + '/'
    response = self.api_client.delete(url, format='json',
      authentication=self.setSession('user2', 123))
    self.assertHttpUnauthorized(response)

  def test_get_groups_authorized(self):
    response = self.api_client.get(self.url,
      format='json', authentication=self.setSession('user1', 123))
    self.assertValidJSONResponse(response)
    result = json.loads(response.content)['objects']
    self.assertEqual(len(result), 2)
    response = self.api_client.get(self.url,
      format='json', authentication=self.setSession('user2', 123))
    self.assertValidJSONResponse(response)
    result = json.loads(response.content)['objects']
    self.assertEqual(len(result), 1)

  def test_create_group_authorized(self):
    user = User.objects.get(username='user1')
    group = {
      'title': 'group create test',
      'items': []
    }
    groups_count = Group.objects.filter(creator=user).count()
    self.assertEqual(groups_count, 2)
    response = self.api_client.post(self.url, format='json',
      data=group, authentication=self.setSession('user1', 123))
    self.assertHttpCreated(response)
    groups_count = Group.objects.filter(creator=user).count()
    self.assertEqual(groups_count, 3)

  def test_put_group_authorized(self):
    user = User.objects.get(username='user1')
    group = Group.objects.get(title='test1')
    url = self.url + str(group.pk) + '/'
    group = self.api_client.get(url, format='json',
      authentication=self.setSession('user1', 123))
    group = self.deserialize(group)
    group['title'] = 'put test'
    response = self.api_client.put(url, format='json',
      data=group, authentication=self.setSession('user1', 123))
    self.assertHttpAccepted(response)

  def test_delete_group_authorized(self):
    user = User.objects.get(username='user1')
    group = Group.objects.get(title='test1')
    groups_count = Group.objects.filter(creator=user).count()
    self.assertEqual(groups_count, 2)
    url = self.url + str(group.pk) + '/'
    response = self.api_client.delete(url, format='json',
      authentication=self.setSession('user1', 123))
    self.assertHttpAccepted(response)
    groups_count = Group.objects.filter(creator=user).count()
    self.assertEqual(groups_count, 1)


class LoginResourceTest(ResourceTestCase):

  def setUp(self):
    super(LoginResourceTest, self).setUp()
    self.login_url = '/api/v1/auth/login/'
    self.logout_url = '/api/v1/auth/logout/'
    user = User.objects.create_user('user1', 'user1@mail.ru', 123)

  def setSession(self, username, password):
    return self.api_client.post('/api/v1/auth/login/',
      format='json', data={"username":username, "password":password})

  def test_delete_MethodNotAllowed(self):
    self.assertHttpMethodNotAllowed(
      self.api_client.delete(self.login_url))

  def test_get_login_MethodNotAllowed(self):
    self.assertHttpMethodNotAllowed(
      self.api_client.get(self.login_url))

  def test_put_login_MethodNotAllowed(self):
    self.assertHttpMethodNotAllowed(
      self.api_client.put(self.login_url))

  def test_post_login_Unauthorized(self):
    self.assertHttpUnauthorized(
      self.api_client.post(self.login_url, format='json',
        data={'username': 'user2', 'password': '123'}))

  def test_post_login_succes(self):
    self.assertHttpOK(self.api_client.post(
        self.login_url, format='json',
          data={'username': 'user1', 'password': '123'}))

  def test_delete_MethodNotAllowed_for_logout(self):
    self.assertHttpMethodNotAllowed(
      self.api_client.delete(self.logout_url))

  def test_post_logout_MethodNotAllowed(self):
    self.assertHttpMethodNotAllowed(
      self.api_client.post(self.logout_url))

  def test_put_logout_MethodNotAllowed(self):
    self.assertHttpMethodNotAllowed(
      self.api_client.put(self.logout_url))

  def test_get_logout_Unauthorized(self):
    self.assertHttpUnauthorized(
      self.api_client.get(self.logout_url))

  def test_get_logout_succes(self):
    self.assertHttpOK(self.api_client.get(
        self.logout_url, format='json',
          authentication=self.setSession('user1', 123)))


class RegisterResourceTest(ResourceTestCase):

  def setUp(self):
    super(RegisterResourceTest, self).setUp()
    self.reg_url = '/api/v1/registration/'
    user1 = User.objects.create_user('user1', 'user1@mail.ru', 123)
    user2 = User.objects.create_user('user2', 'user2@mail.ru', 123)

  def setSession(self, username, password):
    return self.api_client.post('/api/v1/auth/login/', format='json', data={"username":username, "password":password})

  def test_delete_MethodNotAllowed(self):
    self.assertHttpMethodNotAllowed(
      self.api_client.delete(self.reg_url))

  def test_get_MethodNotAllowed(self):
    self.assertHttpMethodNotAllowed(
      self.api_client.get(self.reg_url))

  def test_put_MethodNotAllowed(self):
    self.assertHttpMethodNotAllowed(
      self.api_client.put(self.reg_url))

  def test_registration_fail_user_exist(self):
    response = self.api_client.post(self.reg_url, format='json',
        data={'username' : 'user2', 'password' : '123',
          'confirmPassword' : '123','email' : 'user2@mail.ru'})
    answer = self.deserialize(response)
    self.assertHttpOK(response)
    self.assertEqual(answer["success"], False)

  def test_registration_fail_different_passwords(self):
    self.assertHttpUnauthorized(
      self.api_client.post(
        self.reg_url, format='json',
        data={'username' : 'user3', 'password' : '123',
          'confirmPassword' : '1234','email' : 'user2@mail.ru'}))

  def test_registration_succes(self):
    response = self.api_client.post(
        self.reg_url, format='json',
        data={'username' : 'user3', 'password' : '123',
          'confirmPassword' : '123','email' : 'user2@mail.ru'})
    answer = self.deserialize(response)
    self.assertHttpOK(response)
    self.assertEqual(answer["success"], True)
