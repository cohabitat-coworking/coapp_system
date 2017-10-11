# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from ..serializers import *


# coworkings/{coworking_id}/resources
class ResourcesList(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, format=None):
        resources = Resource.objects.filter(coworking=coworking_id)
        serializer = ResourceSerializer(resources, many=True)
        resources_to_send = {}
        resources_to_send["resources"] = serializer.data
        return Response(resources_to_send)

    def post(self, request, coworking_id, format=None):
        serializer = ResourceCreationSerializer(data=request.data["resource"])

        if serializer.is_valid():
            try:
                coworking = Coworking.objects.get(pk=coworking_id)
                serializer.save(coworking=coworking)
                new_resource = {}
                new_resource["resource"] = serializer.data
                return Response(new_resource, status=status.HTTP_201_CREATED)
            except:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# coworkings/{coworking_id}/resources/{resource_id}
class ResourceDetail(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, resource_id, format=None):
        try:
            resource = Resource.objects.get(pk=resource_id, coworking=coworking_id)
            serializer = ResourceSerializer(resource)
            resource_to_send = {}
            resource_to_send["resource"] = serializer.data
            return Response(resource_to_send)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, coworking_id, resource_id, format=None):
        try:
            resource = Resource.objects.get(pk=resource_id, coworking=coworking_id)
            resource.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, coworking_id, resource_id, format=None):
        try:
            resource = Resource.objects.get(pk=resource_id, coworking=coworking_id)
            serializer = ResourceCreationSerializer(resource, data=request.data["resource"], partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# coworkings/{coworking_id}/resources/{resource_id}/images
class ResourceImageUpload(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, coworking_id, resource_id, format=None):
        try:
            resource = Resource.objects.get(pk=resource_id, coworking_id=coworking_id)
            image_to_upload = request.data['image']
            image = ImageResource(resource=resource)
            image.image = image_to_upload
            image.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# coworkings/{coworking_id}/resources/images/{image_id}/
class ResourceImageDetail(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def delete(self, request, coworking_id, image_id, format=None):
        try:
            image = ImageResource.objects.get(pk=image_id)
            image.image.delete(save=False)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
