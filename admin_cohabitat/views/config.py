from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from backend import models
from backend.models import ContactInfo, Coworking


# admin/confing/{coworking_id}
def config(request, coworking_id):
    try:
        coworking = Coworking.objects.get(pk=coworking_id)
    except ObjectDoesNotExist:
        return render(request, 'not_found.html', status=status.HTTP_404_NOT_FOUND)

    contact_infos = ContactInfo.objects.all()
    data = {'coworking_info': coworking, 'contact_infos': contact_infos}
    return render(
        request,
        'config.html', data
    )
