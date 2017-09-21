# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import *


# coworkings/{coworking_id}/contact_infos
class ContactInfoList(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, format=None):

        try:
            coworking = Coworking.objects.get(pk=coworking_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        contact_info = ContactInfo.objects.filter(coworking=coworking)
        serializer = ContactInfoSerializer(contact_info, many=True)
        contact_infos = {"contact_infos": serializer.data}
        return Response(contact_infos)

    def post(self, request, coworking_id, format=None):
        try:
            coworking = Coworking.objects.get(pk=coworking_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            serializer = ContactInfoCreationSerializer(data=request.data["contact_info"])
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            try:
                coworking = Coworking.objects.get(pk=coworking_id)
                serializer.save(coworking=coworking)
                new_contact = {"contact_info": serializer.data}
                return Response(new_contact, status=status.HTTP_201_CREATED)
            except:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# coworkings/{coworking_id}/contact_types
class ContactTypeList(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, format=None):
        types = ContactType.objects.filter(coworking=coworking_id)
        serializer = ContactTypeSerializer(types, many=True)
        contact_types = {"contact_types": serializer.data}
        return Response(contact_types)


# coworkings/{coworking_id}/contact_infos/{contact_id}
class ContactInfoDetail(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, contact_id, format=None):
        try:
            contact_info = ContactInfo.objects.get(pk=contact_id, coworking=coworking_id)
            serializer = ContactInfoSerializer(contact_info)
            contact_info_to_send = {"contact_info": serializer.data}

            return Response(contact_info_to_send)
            # else:
            #     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  # coworkings/{coworking_id}/plans

    def delete(self, request, coworking_id, contact_id, format=None):

        try:
            coworking = Coworking.objects.get(pk=coworking_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            contact_info = ContactInfo.objects.get(pk=contact_id, coworking=coworking_id)
            contact_info.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, coworking_id, contact_id, format=None):

        try:
            coworking = Coworking.objects.get(pk=coworking_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            contact_info = ContactInfo.objects.get(pk=contact_id, coworking=coworking)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            serializer = ContactInfoCreationSerializer(contact_info, data=request.data["contact_info"], partial=True)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(data={"contact_info": serializer.data}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
