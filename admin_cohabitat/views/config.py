from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status

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


def contact(request, coworking_id):
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    email = request.POST.get("email")

    try:
        coworking = Coworking.objects.get(pk=coworking_id)
    except ObjectDoesNotExist:
        return render(request, "not_found.html")

    ContactInfo.objects.create(name=name, phone=phone, email=email, coworking=coworking)

    return HttpResponseRedirect(reverse('config', kwargs={'coworking_id': coworking_id}))
