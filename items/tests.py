from tastypie.test import ResourceTestCase
from .models import Item
from django.contrib.auth.models import User
import json


class ItemResourceTest(ResourceTestCase):

  def setUp(self):
    super(ItemResourceTest, self).setUp()
    self.url = '/api/v1/item/'
    user = User.objects.create_user("user1", "user1@mail.ru", 123)
    item = Item(description="test description user1", user=user)
    item.save()
    user = User.objects.create_user("user2", "user2@mail.ru", 123)
    item = Item(description="test description user2", user=user)
    item.save()

  def setSession(self, username, password):
    return self.api_client.post('/api/v1/auth/login/', format='json', data={"username":username, "password":password})

  def test_get_list_unauthorized(self):
    self.assertHttpUnauthorized(self.api_client.get(self.url, format='json'))
      
  def test_get_list_authorized(self):
    response = self.api_client.get(self.url, format='json', authentication=self.setSession('user1', 123))
    self.assertValidJSONResponse(response)
    result = json.loads(response.content)['objects']
    self.assertEqual(len(result), 1)

  def test_create_item_unauthorized(self):
    self.assertHttpUnauthorized(self.api_client.post(self.url, format='json', data={}))

  def test_delete_item_unauthorized(self):
    self.assertHttpUnauthorized(self.api_client.delete(self.url + '1/', format='json'))
      
  def test_create_delete_item(self):
    data = {
      'description':'test post_delete description',
    }
    self.assertEqual(Item.objects.filter(user=1).count(), 1)
    self.assertHttpCreated(self.api_client.post(self.url, 
      format='json', authentication=self.setSession('user1', 123), data=data))
    self.assertEqual(Item.objects.filter(user=1).count(), 2)
    pk = Item.objects.filter(description='test post_delete description')[0].pk
    self.assertHttpAccepted(self.api_client.delete(self.url + "%s/" % pk, 
      format='json', authentication=self.setSession('user1', 123)))
    self.assertEqual(Item.objects.filter(user=1).count(), 1)

  def test_put_item_unauthorized(self):
    self.assertHttpUnauthorized(self.api_client.put(self.url + '1/', format='json', data={})) 
      
  def test_put_item(self):
    item = self.deserialize(self.api_client.get(self.url + '1/', 
      format='json', authentication=self.setSession('user1', 123)))
    item['is_completed'] = True
    self.assertHttpAccepted(self.api_client.put(self.url + '1/', format='json',
      authentication=self.setSession('user1', 123), data=item))
    item = self.deserialize(self.api_client.get(self.url + '1/', 
      format='json', authentication=self.setSession('user1', 123)))
    self.assertEqual(item['is_completed'], True)

  def test_get_not_owner(self):
    self.assertHttpUnauthorized(self.api_client.get(self.url + '1/', format="json",
     authentication=self.setSession('user2', 123)))

  def test_put_not_owner(self):
    self.assertHttpUnauthorized(self.api_client.put(self.url + '1/', format='json', 
      data={}, authentication=self.setSession('user2', 123))) 

  def test_delete_not_owner(self):
    self.assertHttpUnauthorized(self.api_client.delete(self.url + '1/', format='json', 
      authentication=self.setSession('user2', 123)))    
