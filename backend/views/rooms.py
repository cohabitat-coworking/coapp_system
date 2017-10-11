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

# coworkings/{coworking_id}/rooms
class RoomsList(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, format=None):
        rooms = Room.objects.filter(coworking=coworking_id)
        serializer = RoomSerializer(rooms, many=True)
        rooms_to_send = {}
        rooms_to_send["rooms"] = serializer.data
        return Response(rooms_to_send)

    def post(self, request, coworking_id, format=None):
        serializer = RoomCreationSerializer(data=request.data["room"])

        if serializer.is_valid():
            # try:
            coworking = Coworking.objects.get(pk=coworking_id)
            serializer.save(coworking=coworking)
            new_room = {}
            new_room["room"] = serializer.data
            return Response(new_room, status=status.HTTP_201_CREATED)
            # except:
            #     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# coworkings/{coworking_id}/room_types
class RoomTypesList(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, format=None):
        types = RoomType.objects.filter(coworking=coworking_id)
        serializer = RoomTypeSerializer(types, many=True)

        room_types = {}
        room_types["room_types"] = serializer.data
        return Response(room_types)


# coworkings/{coworking_id}/rooms/{room_id}
class RoomDetail(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, room_id, format=None):
        try:
            room = Room.objects.get(pk=room_id, coworking=coworking_id)
            serializer = RoomSerializer(room)
            room_to_send = {}
            room_to_send["room"] = serializer.data
            return Response(room_to_send)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, coworking_id, room_id, format=None):
        try:
            room = Room.objects.get(pk=room_id, coworking=coworking_id)
            room.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, coworking_id, room_id, format=None):
        try:
            room = Room.objects.get(pk=room_id, coworking=coworking_id)
            serializer = RoomCreationSerializer(room, data=request.data["room"], partial=True)
            if serializer.is_valid():
                serializer.save()
                patched_room = {"room" : serializer.data}
                return Response(data=patched_room, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# coworkings/{coworking_id}/rooms/{room_id}/images
class RoomImageUpload(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, coworking_id, room_id, format=None):
        try:
            room = Room.objects.get(pk=room_id, coworking_id=coworking_id)
            image_to_upload = request.data['image']
            image = ImageRoom(room=room)
            image.image = image_to_upload
            image.save()
            image_data = ImageRoomSerializer(image)
            return Response(data=image_data.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# coworkings/{coworking_id}/rooms/images/{image_id}/
class RoomImageDetail(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def delete(self, request, coworking_id, image_id, format=None):
        try:
            image = ImageRoom.objects.get(pk=image_id)
            image.image.delete(save=False)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
