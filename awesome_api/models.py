from django.db import models
from datetime import datetime
import uuid
import json
# Create your models here.


def generate_no_with_datetime(prefix):
    time = datetime.now()
    format_time = time.strftime('%Y%m%d%H%M%S')
    return f'{prefix}{format_time}'


class JsonField(models.Field):
    """
    Json field
    """
    description = 'Accept json strong'

    def db_type(self, connection):
        return 'json'

    def to_python(self, value):
        if value is None:
            return value
        return json.loads(value)

    def get_prep_value(self, value):
        return json.dumps(value)


class BaseInfoModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(
        '创建时间', auto_now_add=True, editable=False)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    is_active = models.BooleanField('是否启用', default=True)
    is_delete = models.BooleanField('是否删除', default=False)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        abstract = True


METHODS = (
    ('GET', 'GET'),
    ('POST', 'POST'),
)


class Project(BaseInfoModel):
    project_name = models.CharField('项目名称', max_length=255)
    project_description = models.TextField('项目描述', blank=True)

    def __str__(self):
        return self.project_name


class Module(BaseInfoModel):
    module_name = models.CharField('模块名称', max_length=100)
    module_description = models.TextField('模块描述', blank=True)
    module_project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.module_name


class TestCase(BaseInfoModel):
    case_no = models.CharField(
        '用例编号', max_length=255, default=generate_no_with_datetime('CASE'), editable=False)
    case_name = models.CharField('用例名称', max_length=255)
    case_description = models.TextField('用例描述', blank=True)
    case_method = models.CharField('请求方式', choices=METHODS, max_length=6)
    case_path = models.CharField('请求路径', max_length=255)
    case_headers = models.CharField('请求头', max_length=512, blank=True)
    case_params = models.CharField('请求参数', max_length=512, blank=True)
    case_body = models.CharField('请求内容', max_length=512, blank=True)
    case_assert = models.CharField('断言', max_length=255, blank=True)
    case_module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return self.case_name

    def case_no_generate(self):
        pass


class Environment(BaseInfoModel):
    env_name = models.CharField('环境名称', max_length=255)
    env_host = models.CharField('环境地址', max_length=255)
    env_login_endpoint = models.CharField('登录地址', max_length=255)
    env_login_username = models.CharField('登录用户名', max_length=255)
    env_login_password = models.CharField('登录密码', max_length=255)
    env_description = models.TextField('环境描述', blank=True)

    def __str__(self):
        return self.env_name


class Database(BaseInfoModel):
    db_connect_name = models.CharField('数据库连接名', max_length=255)
    db_name = models.CharField('数据库名', max_length=255)
    db_host = models.CharField('数据库地址', max_length=255)
    db_port = models.CharField('数据库端口', max_length=255)
    db_username = models.CharField('用户名', max_length=255)
    db_password = models.CharField('密码', max_length=255)

    def __str__(self):
        return self.db_connect_name


class EmailContent(BaseInfoModel):
    email_subject = models.CharField('邮件主题', max_length=255)
    email_content = models.TextField('邮件内容')
    email_receivers_pass = models.CharField(
        '通过发送人', max_length=512, blank=True)
    email_receivers_fail = models.CharField(
        '失败发送人', max_length=512, blank=True)

    def __str__(self):
        return self.email_subject


class Task(BaseInfoModel):
    task_no = models.CharField(
        '任务编号', max_length=255, default=generate_no_with_datetime('TASK'), editable=False)
    task_name = models.CharField('任务名称', max_length=255)
    task_remak = models.CharField('备注', max_length=255)
    task_start_time = models.DateTimeField('开始时间')
    task_stop_time = models.DateTimeField('结束时间')

    task_env = models.ForeignKey(Environment, on_delete=models.CASCADE)
    task_cases = models.ManyToManyField(TestCase)

    def __str__(self):
        return self.task_name



