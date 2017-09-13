from django.conf import settings
from django.db import models
from oauth2_provider.models import AbstractAccessToken


# Utility function to add :read variats if :write exists
def update_scopes(scopes):
    read_scopes = []
    for scope in scopes:
        if scope.endswith(':write'):
            read_scope = scope.replace(':write', ':read')

            if read_scope not in scopes:
                read_scopes.append(read_scope)
    return scopes + read_scopes


# Check if scope is allowed for user type
def check_allowed_scope(required_scopes, user_type='uncategorized'):
    allowed_scopes = settings.APPUNTA_ALLOWED_SCOPES[user_type]
    allowed_scopes = set(update_scopes(allowed_scopes))
    return set(required_scopes).issubset(allowed_scopes)


class Teacher(models.Model):
    user = models.OneToOneField("auth.User",
                                on_delete=models.CASCADE,
                                related_name='teacher')

    def __str__(self):
        return self.user.get_full_name()


class AppuntaAccessToken(AbstractAccessToken):
    """
    An AccessToken instance represents the actual access token to
    access user's resources, as in :rfc:`5`.
    Fields:
    * :attr:`user` The Django user representing resources' owner
    * :attr:`token` Access token
    * :attr:`application` Application instance
    * :attr:`expires` Date and time of token expiration, in DateTime format
    * :attr:`scope` Allowed scopes
    """

    def save(self, *args, **kwargs):
        updated_scopes = update_scopes(self.scope.split())
        self.scope = ' '.join(updated_scopes)
        super(AppuntaAccessToken, self).save(*args, **kwargs)

    def allow_scopes(self, scopes):
        print(scopes)
        """
        Check if the token allows the provided scopes
        :param scopes: An iterable containing the scopes to check
        """
        if not scopes:
            return True

        user_types = (
            'teacher',
            'student'
        )
        categorized = False

        # Only the correct type of user can access to different resources
        for user_type in user_types:
            print(user_type)
            if hasattr(self.user, user_type):
                categorized = True

                if not check_allowed_scope(scopes, user_type):
                    self.revoke()
                    return False

                break  # It should be only one type

        if not categorized and not check_allowed_scope(scopes):
            self.revoke()
            return False

        # Let OAuth toolkit do the rest
        return super(AppuntaAccessToken, self).allow_scopes(scopes)

