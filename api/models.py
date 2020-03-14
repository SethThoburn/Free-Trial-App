from django.db import models

class Trial(models.Model):
    name = models.CharField(max_length=256)
    url = models.URLField(blank=True, null=True)
    period = models.IntegerField()
    value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class TrialInstance(models.Model):
    trial = models.ForeignKey('Trial', on_delete=models.CASCADE)
    email = models.EmailField()
    session_id = models.CharField(max_length=128, null=True, blank=True)
    executor_url = models.CharField(max_length=128, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)