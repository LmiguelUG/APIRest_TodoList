from django.db import models
from helpers.models import TrackingModel
from django.contrib.auth.models import (PermissionsMixin, AbstractBaseUser, UserManager)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class MyUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """ Create and save a user with the given username, email, and password. """
        if not username:
            raise ValueError('The given username must be set')

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
            
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    
    username_validator = UnicodeUsernameValidator()
    email = models.EmailField(_('email address'), blank = False, unique = True)
    username = models.CharField(_('username'), max_length = 150, unique = True, validators=[username_validator])
    password = models.CharField(_('password'), max_length = 100)
    is_staff = models.BooleanField(_('staff status'), default = False)
    is_active = models.BooleanField(_('active'), default = True)
    email_verified = models.BooleanField(_('email verified'), default = False)
    date_joined = models.DateTimeField(_('date joined'), default = timezone.now)

    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    @property
    def token(self):
        return ''
