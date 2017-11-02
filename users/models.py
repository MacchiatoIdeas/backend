from django.db import models
from oauth2_provider.models import AbstractAccessToken

class AppuntaUser(models.Model):
    birth_date = models.DateField(null=True, blank=True)
    institution = models.CharField(max_length=128)
    avatar = models.ImageField(null=True, blank=True)

    class Meta:
        abstract = True


class AppuntaTeacher(AppuntaUser):
    user = models.OneToOneField("auth.User",
                                on_delete=models.CASCADE,
                                related_name='teacher')

    rut = models.CharField(max_length=16)
    # CV - pendiente
    bio = models.CharField(max_length=140)

    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()


class AppuntaStudent(AppuntaUser):
    user = models.OneToOneField("auth.User",
                                on_delete=models.CASCADE,
                                related_name='student')

    def __str__(self):
        return self.user.get_full_name()
