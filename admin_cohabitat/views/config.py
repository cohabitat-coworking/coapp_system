from django.shortcuts import render

from backend import models
from backend.models import ContactInfo, Coworking


def config(request):
    coworking = Coworking.objects.all().first()
    contact_infos = ContactInfo.objects.all()


    data = {'coworking_info': coworking, 'contact_infos': contact_infos}
    return render(
        request,
        'config.html', data
    )
