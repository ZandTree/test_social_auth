# C:\Users\tanja\Desktop\pycharmProjects\store\users
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    # kwargs are: {'username': '***'}
    def create_user(self, email, password=None, **kwargs):
        """
        Create and save a User with the given email and password.
        kwargs no need; pure for social_auth
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user
