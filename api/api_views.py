from rest_framework import viewsets
from . import models
from . import serializers

class TrialViewset(viewsets.ModelViewSet):
    queryset = models.Trial.objects.all()
    serializer_class = serializers.TrialSerializer