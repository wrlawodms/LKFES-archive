from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=100)
	desc = models.CharField(max_length=500, default="description")
	reporter = models.CharField(max_length=20)
	pub_date = models.DateTimeField('date published', auto_now_add=True)

	def __str__(self):
		return self.title+' - by '+self.reporter

