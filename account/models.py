from django.contrib.auth.models import AbstractUser
from django.db import models
from pkg_resources import _

from account.utils import generate_jti


class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=50)
    is_manager = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # jti - JWT identifier
    jti = models.CharField(_("jwt id"), max_length=64, blank=False, null=False, editable=False, default=generate_jti,
                           help_text=_("JWT tokens for the user get revoked when JWT id has regenerated."),
                           )

    def __str__(self):
        return f"{self.id} - {self.username}"


class Person:
    def __init__(self, name):
        self.name = name