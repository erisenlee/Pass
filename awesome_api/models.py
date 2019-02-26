from django.db import models
import uuid
# Create your models here.


class BaseInfoModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(
        'created_time', auto_now_add=True, editable=False)
    updated_at = models.DateTimeField('updated_time', auto_now=True)
    is_active = models.BooleanField('is_active', default=True)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        abstract = True


METHODS = (
    ('GET', 'GET'),
    ('POST', 'POST'),
)


class Project(BaseInfoModel):
    name = models.CharField('name', max_length=100)
    info = models.TextField('infomations', null=True, blank=True)

    def __str__(self):
        return self.name


class Module(BaseInfoModel):
    name = models.CharField('name', max_length=100)
    info = models.TextField('infomations', null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Name(BaseInfoModel):
    name = models.CharField('name', max_length=100)
    method = models.CharField('method', choices=METHODS, max_length=6)
    path = models.URLField('path')
    headers = models.CharField('headers', max_length=512)
    params = models.CharField('params', max_length=512)
    body = models.CharField('body', max_length=512)
    key = models.AutoField('key')
    module_src = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    