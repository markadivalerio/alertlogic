from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Search(models.Model):
	title = models.CharField(max_length=100, blank=True, default='')
	person = models.CharField(max_length=100, blank=True, default='')