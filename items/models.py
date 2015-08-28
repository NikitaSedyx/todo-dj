from django.db import models
from django.contrib.auth.models import User
from tastypie.utils.timezone import now
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

class Group(models.Model):
  creator = models.ForeignKey(User, related_name='creator')
  users = models.ManyToManyField(User)
  created_at = models.DateTimeField(auto_now_add=True, editable=False)
  updated_at = models.DateTimeField(auto_now=True, editable=False)
  title = models.CharField(max_length=150, default='Group Tasks')
  view = models.BooleanField(default=True)
  is_deleted = models.BooleanField(default=False)
  RED = 'red'
  GREEN = 'green'
  BLUE = 'blue'
  ORANGE = 'orange'
  WHITE = 'white'
  YELLOW = 'yellow'
  COLORS = (
    (RED, RED),
    (GREEN, GREEN),
    (BLUE, BLUE),
    (ORANGE, ORANGE),
    (WHITE, WHITE),
    (YELLOW, YELLOW),
  )
  color = models.CharField(max_length=6, choices=COLORS, default=WHITE)

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


class File(models.Model):
  filename = models.CharField(max_length=150, default='')
  file = models.FileField(upload_to='./', null=True)
  group = models.ForeignKey(Group)

  class Meta:
    db_table = 'todo_files'

  def __str__(self):
    return self.filename


@receiver(pre_delete, sender=File)
def delete_file(sender, instance, **kwargs):
    instance.file.delete(True)
