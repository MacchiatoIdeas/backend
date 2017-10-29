from django.db import models
from oauth2_provider.models import AbstractAccessToken


class Teacher(models.Model):
    user = models.OneToOneField("auth.User",
                                on_delete=models.CASCADE,
                                related_name='teacher')

    def __str__(self):
        return self.user.get_full_name()


class AppuntaAdmin(models.Model):
    user = models.OneToOneField("auth.User",
                                on_delete=models.CASCADE,
                                related_name='appunta_admin')


class AvatarLink(models.Model):
    user = models.OneToOneField("auth.User",
                                on_delete=models.CASCADE,
                                related_name='avatar_link')
    avatar = models.ImageField(null=True)