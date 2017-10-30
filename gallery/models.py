from django.db import models

# Create your models here.
class Gallery(models.Model):
	user = models.ForeignKey('auth.User',
	                         on_delete=models.CASCADE,
	                         related_name='images')

	image = models.ImageField()