# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import *


# coworkings/
class CoworkingList(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        coworkings = Coworking.objects.all()
        serializer = CoworkingSerializer(coworkings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        try:
            serializer = CoworkingCreationSerializer(data=request.data["coworking"])
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            coworking = {"coworking": serializer.data}
            return Response(coworking, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# coworkings/{coworking_id}
class CoworkingDetail(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, format=None):
        try:
            coworking = Coworking.objects.get(pk=coworking_id)
            serializer = CoworkingSerializer(coworking)
            coworking_to_send = {}
            coworking_to_send["coworking"] = serializer.data
            return Response(coworking_to_send)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, coworking_id, format=None):
        try:
            coworking = Coworking.objects.get(pk=coworking_id)
            coworking.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, coworking_id, format=None):
        try:
            coworking = Coworking.objects.get(pk=coworking_id)
            serializer = CoworkingCreationSerializer(coworking, data=request.data["coworking"], partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"coworking": serializer.data}, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
