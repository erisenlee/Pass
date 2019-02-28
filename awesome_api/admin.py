from django.contrib import admin
from . models import TestCase, Project, Module, Environment, Database, Task
# Register your models here.

admin.site.register([TestCase, Project, Module, Environment, Database, Task])