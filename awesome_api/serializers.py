from rest_framework import serializers
from . models import TestCase

class TestCaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TestCase
        exclude = ['case_module']


