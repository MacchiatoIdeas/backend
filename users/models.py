from django.db import models


class Teacher(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()
