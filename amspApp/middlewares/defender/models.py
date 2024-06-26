from __future__ import unicode_literals

from django.db import models
# from django.utils.encoding import python_2_unicode_compatible
from six import python_2_unicode_compatible


@python_2_unicode_compatible
class AccessAttempt(models.Model):
    user_agent = models.CharField(
        max_length=255,
    )
    ip_address = models.GenericIPAddressField(
        verbose_name='IP Address',
        null=True,
    )
    username = models.CharField(
        max_length=255,
        null=True,
    )
    http_accept = models.CharField(
        verbose_name='HTTP Accept',
        max_length=1025,
    )
    path_info = models.CharField(
        verbose_name='Path',
        max_length=255,
    )
    attempt_time = models.DateTimeField(
        auto_now_add=True,
    )
    login_valid = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ['-attempt_time']

    def __str__(self):
        """ unicode value for this model """
        return "{0} @ {1} | {2}".format(self.username,
                                        self.attempt_time,
                                        self.login_valid)
