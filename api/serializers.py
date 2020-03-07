from rest_framework import serializers
from . import models

class TrialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Trial
        fields = (
            'id',
            'name',
            'url',
            'period',
            'value',
        )