from django.db import models

class Trial(models.Model):
    name = models.CharField(max_length=256)
    url = models.URLField(blank=True, null=True)
    period = models.IntegerField()
    value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name