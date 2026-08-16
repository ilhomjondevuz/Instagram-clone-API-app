import random
import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.shared.models import BaseModel


ORDINARY, MANAGER, ADMIN = 'ordinary', 'manager', 'admin'

VIA_PHONE_NUMBER, VIA_EMAIL, VIA_USERNAME = (
    'via_phone_number',
    'via_email',
    'via_username',
)

NEW, CODE_VERIFIED, DONE, PHOTO_DONE = (
    'new',
    'code_verified',
    'done',
    'photo_done',
)

MALE, FEMALE, OTHER = 'M', 'F', 'O'


class User(AbstractUser, BaseModel):
    USER_ROLES = (
        (ORDINARY, ORDINARY),
        (MANAGER, MANAGER),
        (ADMIN, ADMIN),
    )
    AUTH_TYPES = (
        (VIA_PHONE_NUMBER, VIA_PHONE_NUMBER),
        (VIA_EMAIL, VIA_EMAIL),
    )
    AUTH_STATUSES = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
        (PHOTO_DONE, PHOTO_DONE),
    )
    GENDER_CHOICES = (
        (MALE, MALE),
        (FEMALE, FEMALE),
        (OTHER, OTHER),
    )
    role = models.CharField(
        max_length=8,
        choices=USER_ROLES,
        default=ORDINARY,
    )
    auth_type = models.CharField(
        max_length=16,
        choices=AUTH_TYPES,
    )
    auth_status = models.CharField(
        max_length=13,
        choices=AUTH_STATUSES,
        default=NEW,
    )
    phone_number = models.CharField(
        max_length=13,
        null=True,
        blank=True,
        unique=True,
    )
    email = models.EmailField(
        null=True,
        blank=True,
        unique=True,
    )
    bio = models.TextField(
        null=True,
        blank=True,
    )
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to='avatars/%Y/%m',
        validators=[
            FileExtensionValidator(
                ['png', 'jpg', 'jpeg']
            )
        ],
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.username

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    def create_verify_code(self, verify_type):
        code = ''.join(
            str(random.randint(0, 9))
            for _ in range(4)
        )

        if verify_type == VIA_PHONE_NUMBER:
            expiration_time = (
                    timezone.now()
                    + timedelta(minutes=PHONE_EXPIRE)
            )
        elif verify_type == VIA_EMAIL:
            expiration_time = (
                timezone.now()
                + timedelta(minutes=EMAIL_EXPIRE)
            )
        else:
            expiration_time = timezone.now() + timedelta(minutes=EMAIL_EXPIRE)

        UserConfirmation.objects.update_or_create(
            user=self,
            verify_type=verify_type,
            code=code,
            is_confirmed=False,
            expiration_time=expiration_time
        )

        return code

    def check_username(self):
        if not self.username:
            self.username = f'username_{uuid.uuid4().hex[:12]}'

    def check_pass(self):
        if not self.password:
            self.password = f'password_{uuid.uuid4().hex}'

    def hashing_password(self):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)

    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def clean(self):
        self.check_username()
        self.check_pass()
        self.hashing_password()

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.clean()

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('-date_joined',)


PHONE_EXPIRE = 2
EMAIL_EXPIRE = 5

class UserConfirmation(BaseModel):

    VERIFY_TYPES = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE_NUMBER, VIA_PHONE_NUMBER),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="confirmations"
    )
    verify_type = models.CharField(
        max_length=16,
        choices=VERIFY_TYPES,
    )
    code = models.CharField(
        max_length=4,
    )
    expiration_time = models.DateTimeField()
    is_confirmed = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f'{self.user.username} - {self.is_confirmed}'

    def save(self, *args, **kwargs):
        if self._state.adding:

            if self.verify_type == VIA_PHONE_NUMBER:
                self.expiration_time = (
                    timezone.now()
                    + timedelta(minutes=PHONE_EXPIRE)
                )

            elif self.verify_type == VIA_EMAIL:
                self.expiration_time = (
                    timezone.now()
                    + timedelta(minutes=EMAIL_EXPIRE)
                )

            else:
                raise ValidationError(
                    'Verification type not supported.'
                )

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'user_confirmations'
        verbose_name = 'user confirmation'
        verbose_name_plural = 'user confirmations'
        ordering = ('-expiration_time',)