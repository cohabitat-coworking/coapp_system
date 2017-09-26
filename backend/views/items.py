# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import *


# coworkings/{coworking_id}/items/{item_id}
class ItemDetail(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, item_id, format=None):
        try:
            item = Item.objects.get(pk=item_id, coworking=coworking_id)
            serializer = ItemSerializer(item)
            item_to_send = {}
            item_to_send["item"] = serializer.data
            return Response(item_to_send)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, coworking_id, item_id, format=None):
        try:
            item = Item.objects.get(pk=item_id, coworking=coworking_id)
            item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, coworking_id, item_id, format=None):
        try:
            item = Item.objects.get(pk=item_id, coworking=coworking_id)
            serializer = ItemCreationSerializer(item, data=request.data["item"], partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# coworkings/{coworking_id}/items
class ItemsList(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, format=None):
        items = Item.objects.filter(coworking=coworking_id)
        serializer = ItemSerializer(items, many=True)
        items_to_send = {}
        items_to_send["items"] = serializer.data
        return Response(items_to_send)

    def post(self, request, coworking_id, format=None):
        serializer = ItemCreationSerializer(data=request.data["item"])

        if serializer.is_valid():
            try:
                coworking = Coworking.objects.get(pk=coworking_id)
                serializer.save(coworking=coworking)
                new_item = {}
                new_item["item"] = serializer.data
                return Response(new_item, status=status.HTTP_201_CREATED)
            except:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# coworkings/{coworking_id}/item_types
class ItemTypesList(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, format=None):
        types = ItemType.objects.filter(coworking=coworking_id)
        serializer = ItemTypeSerializer(types, many=True)
        item_types = {}
        item_types["item_types"] = serializer.data
        return Response(item_types)

# coworkings/{coworking_id}/items/{item_id}/images
class ItemImageUpload(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, coworking_id, item_id, format=None):
        try:
            item = Item.objects.get(pk=item_id, coworking_id=coworking_id)
            image_to_upload = request.data['image']
            image = ImageItem(item=item)
            image.image = image_to_upload
            timestr = str(datetime.now())
            image.image.name = timestr + "-" + image.image.name
            image.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# coworkings/{coworking_id}/items/images/{image_id}/
class ItemImageDetail(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def delete(self, request, coworking_id, image_id, format=None):
        try:
            image = ImageItem.objects.get(pk=image_id)
            image.image.delete(save=False)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


