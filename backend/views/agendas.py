# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import *


class AgendaRooms(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, format=None):
        agendas = AgendaRoom.objects.all()
        serializers = AgendaRoomSerializer(agendas, many=True)
        return Response(serializers.data)


# coworkings/{oworking_id}/agenda_resources
class AgendaResources(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, format=None):
        agendas = AgendaResource.objects.all()
        serializers = AgendaResourceSerializer(agendas, many=True)
        return Response(serializers.data)


# coworkings/{oworking_id}/agenda_items
class AgendaItems(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, format=None):
        agendas = AgendaItem.objects.all()
        serializers = AgendaItemSerializer(agendas, many=True)
        return Response(serializers.data)
