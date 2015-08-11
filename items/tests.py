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
