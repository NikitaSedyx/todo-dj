from django.test import TestCase
from .models import Item, Group
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError


class ItemModelTest(TestCase):

  def setUp(self):
    super(ItemModelTest, self).setUp()
    user = User.objects.create_user('user', 'u@u', 123)
    group = Group(creator=user)
    group.save()

  def test_create_item(self):
    group = Group.objects.all()[0]
    self.assertEqual(Item.objects.all().count(), 0)
    item = Item(group=group)
    item.save()
    self.assertEqual(Item.objects.all().count(), 1)

  def test_create_item_default_description(self):
    group = Group.objects.all()[0]
    item = Item(group=group)
    self.assertEqual(item.description, '')

  def test_create_item_default_is_completed(self):
    group = Group.objects.all()[0]
    item = Item(group=group)
    self.assertFalse(item.is_completed)

  def test_create_item_auto_created_at(self):
    group = Group.objects.all()[0]
    item = Item(group=group)
    item.save()
    self.assertLess(item.created_at, timezone.now())

  def test_create_item_default_deadline(self):
    group = Group.objects.all()[0]
    item = Item(group=group)
    self.assertLess(item.deadline, timezone.now())

  def test_create_item_non_group(self):
    item = Item()
    self.assertRaises(IntegrityError, item.save)
