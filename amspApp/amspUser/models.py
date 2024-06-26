# encoding=utf8
from datetime import datetime

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from mongoengine import *

from amspApp.CompaniesManagment.models import Company
from amspApp.MyProfile.models import Profile
from django.contrib import admin


class MyUserManager(BaseUserManager):



    def create_user(self,
                    username,
                    email,
                    password=None,
                    confirm_password=None
                    ):

        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_active=True,
        )

        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(username, email,
                                password=password,
                                )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=255, unique=True,
                                help_text=_('Required. 30 characters or fewer. Letters, digits and only.'),
                                validators=[
                                    validators.RegexValidator(r'^[-a-zA-Z0-9_]+$',
                                                              _('Enter a valid username. '
                                                                'This value may contain only letters, numbers '
                                                                'and - and _ characters.'), 'invalid'),
                                ],
                                error_messages={
                                    'unique': _("A user with that username already exists."),
                                })
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=False, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    is_deleted = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    sign_password_before_confirm = models.CharField(max_length=500, blank=True, null=True)
    sign_password = models.CharField(_('sign password'), max_length=500, blank=True, null=True)
    sign_password_confirmsms = models.CharField(max_length=500, blank=True, null=True)
    is_sign_pass_correct = models.BooleanField(default=False)
    timezone = models.CharField(max_length=30, blank=True, null=True, default="Asia/Tehran")
    password_reset = models.CharField(max_length=120, blank=True, null=True)
    password_reset_post_date = models.DateTimeField(blank=True, null=True)
    current_company = models.ForeignKey(to=Company, null=True, blank=True)
    personnel_code = models.CharField(max_length=20, blank=True, null=True, default="0")
    cellphone = models.CharField(max_length=500, blank=True, null=True)
    """
    AccountType
    1 = automation
    2 = First Try
    4 = supplier seller
    5 = supplier service
    6 = supplier factory
    7 = hire
    """
    account_type = models.IntegerField(default=1, blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_user_profile(self):
        return Profile.objects.get(userID=self.id)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


# from django.contrib.auth.admin import UserAdmin
# admin.site.register(MyUser, UserAdmin)


class positionIDLastActivities(Document):
    positionID = IntField(required=True, )
    companyID = IntField(required=True, )
    dateOfPost = DateTimeField(default=timezone.now())


class FirstReg(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    cellNo = StringField(unique=True)
    password = StringField()
    gencode = StringField()
    hash = StringField()
    verifyTry = IntField(default=0)


class ForgetPassCodes(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    cellNo = StringField(unique=True)
    userID = IntField(required=True)
    gencode = StringField()
    verifyTry = IntField(default=0)
    hash = StringField()


class BasicAuths(Document):
    userID = IntField(required=True, )
    deviceType = StringField()
    token = StringField()
    dateOfPost = DateTimeField(default=datetime.now())
