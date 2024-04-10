from datetime import datetime

from django.db import models

# Create your models here.
from mongoengine import Document, DateTimeField, DictField, StringField, IntField


class Languages(models.Model):
    en = models.TextField(max_length=2000, null=True, blank=True)
    fa = models.TextField(max_length=2000, null=True, blank=True)
    ar = models.TextField(max_length=2000, null=True, blank=True)
    kr = models.TextField(max_length=2000, null=True, blank=True)


class Sidebar(models.Model):
    name = models.TextField(max_length=50)
    state = models.TextField(max_length=50)
    type = models.TextField(max_length=50)
    icon = models.TextField(max_length=50)
    parent = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)


class Helpbar(models.Model):
    url = models.TextField(max_length=550)
    angularUrl = models.TextField(max_length=550)
    title = models.TextField(max_length=550)
    help_fa = models.TextField(max_length=2000)
    help_en = models.TextField(max_length=2000)
    link_fa = models.TextField(max_length=450)
    link_en = models.TextField(max_length=450)


