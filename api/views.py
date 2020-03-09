from django.shortcuts import render
from django.http import HttpResponse
from .models import Trial


def email(request):
    if request.method == 'POST':
        print(request.POST)
        subject = request.POST.get('subject', '')
        Trial.objects.create(
            name = subject,
            period = 30,
        )
    return HttpResponse()