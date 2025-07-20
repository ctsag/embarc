from django.shortcuts import render
from adventures.models import Adventure, Mission


def index(request):
    return render(
        request,
        'index.html',
        {
            'adventure_count': Adventure.objects.count(),
            'mission_count': Mission.objects.count()
        }
    )
