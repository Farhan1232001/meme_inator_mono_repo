from uuid import uuid7
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user_name, email, password, **extra_fields):
        if not user_name:
            raise ValueError("The user_name must be set")
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(user_name=user_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(user_name, email, password, **extra_fields)

    def create_superuser(self, user_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(user_name, email, password, **extra_fields)


class UserModel(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that maps to the OpenAPI spec.
    Primary identifier is `user_name`.
    """
    id = models.UUIDField(primary_key=True, default=uuid7)
    user_name = models.CharField(_("user name"), max_length=150, unique=True)
    email = models.EmailField(_("email address"), unique=True)

    # Business flags from OpenAPI
    is_online = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    # Entitlements in authoization application now manages this
    # is_pro_user = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()
    
    # TODO: redundant since is_active tracks whether user in use or not. 
    is_soft_deleted = models.BooleanField(default=False)

    # Django admin flags ()
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )


    USERNAME_FIELD = "user_name"
    REQUIRED_FIELDS = ["email"]  # email required when creating superusers via createsuperuser

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_short_name(self):
        return self.first_name or self.user_name

    def __str__(self):
        return f"{self.user_name} <{self.email}>"

