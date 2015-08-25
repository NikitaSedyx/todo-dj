from django.db import models
from django.contrib.auth.models import User
from tastypie.utils.timezone import now

class Group(models.Model):
  creator = models.ForeignKey(User, related_name='creator')
  users = models.ManyToManyField(User)
  created_at = models.DateTimeField(auto_now_add=True, editable=False)
  updated_at = models.DateTimeField(auto_now=True, editable=False)
  title = models.CharField(max_length=150, default='Group Tasks')
  view = models.BooleanField(default=True)
  is_deleted = models.BooleanField(default=False)

  class Meta:
    db_table = 'todo_groups'
    ordering = ['-created_at']

  def __str__(self):
    return self.title


class Item(models.Model):
  created_at = models.DateTimeField(auto_now_add=True, editable=False)
  description = models.TextField()
  is_completed = models.BooleanField(default=False)
  deadline = models.DateTimeField(default=now)
  group = models.ForeignKey(Group)
  
  class Meta:
    db_table = 'todo_items'
    ordering = ['is_completed', 'deadline']

  def __str__(self):
    return self.description
