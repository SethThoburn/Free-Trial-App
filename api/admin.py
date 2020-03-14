from django.contrib import admin

from .models import Trial, TrialInstance

admin.site.register(Trial)
admin.site.register(TrialInstance)