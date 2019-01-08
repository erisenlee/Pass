from django.db import models
from django.core import signing
from django.contrib.auth.models import User
import uuid

# Create your models here.


class BaseInfoModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(
        'created_time', auto_now_add=True, editable=False)
    updated_at = models.DateTimeField('updated_time', auto_now=True)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        abstract = True


class AccountManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Account(BaseInfoModel):

    name = models.CharField('Name', max_length=255)
    link = models.URLField('website')
    username = models.CharField('account_user', max_length=255)
    password = models.CharField('account_password', max_length=255)
    description = models.CharField(
        'info', max_length=255, null=True, blank=True)
    is_active = models.BooleanField('is_active', default=True)
    tags = models.ManyToManyField('Tag')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # active_manager = AccountManager()
    objects = models.Manager()

    class Meta(BaseInfoModel.Meta):
        indexes = [
            models.Index(fields=['name', 'link'])
        ]

    def save(self, *args, **kwargs):
        self.password = self.sign_password(self.password)
        super().save(*args, **kwargs)

    def sign_password(self, password):
        value = signing.dumps(password)
        return value

    def unsign_password(self, sign_value):
        value = signing.loads(sign_value)
        return value

    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return '{} {}'.format(self.__class__, self.name)


class Tag(BaseInfoModel):
    name = models.CharField('tag_name', max_length=64, unique=True)
    is_active = models.BooleanField('is_active', default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta(BaseInfoModel.Meta):
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name

    def __repr__(self):
        return '{} {}'.format(self.__class__, self.name)
