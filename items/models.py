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
    