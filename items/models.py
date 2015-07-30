from django.db import models
from django.contrib.auth.models import User
from tastypie.utils.timezone import now

class Item(models.Model):
  user = models.ForeignKey(User)
  created_at = models.DateTimeField(auto_now_add=True, editable=False)
  description = models.CharField(max_length=150, default='')
  is_completed = models.BooleanField(default=False)
  deadline = models.DateTimeField(default=now)

  class Meta:
    db_table = 'todo_items'
    ordering = ['is_completed', 'deadline']

  def __str__(self):
    return self.description

class Group(models.Model):
  users = models.ManyToManyField(User)
  created_at = models.DateTimeField(auto_now_add=True, editable=False)
  updated_at = models.DateTimeField(auto_now=True, editable=False)
  title = models.CharField(max_length=150, default='Group Tasks')
  items = models.ManyToManyField(Item)
  view = models.BooleanField(default=True)
  is_deleted = models.BooleanField(default=False)

  class Meta:
    db_table = 'todo_groups'
    ordering = ['-created_at']

  def __str__(self):
    return self.title


