# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import *


# coworkings/{oworking_id}/schedulings
class QuerySchedulings(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, format=None):
        agendas = Agenda.objects.filter(coworking=coworking_id)
        serializer = QueryAgendaSerializer(agendas, many=True)
        schedulings_to_send = {}
        schedulings_to_send["schedulings"] = serializer.data
        return Response(schedulings_to_send)


class QuerySpecificScheduling(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, agenda_id, format=None):
        try:
            agenda = Agenda.objects.get(coworking_id=coworking_id, pk=agenda_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized_agenda = {"scheduling": QueryAgendaSerializer(agenda).data}
        return Response(data=serialized_agenda, status=status.HTTP_200_OK)


# coworkings/{oworking_id}/room_schedulings/{room_id}
class QueryRoomSchedulings(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, room_id, format=None):
        try:
            room = Room.objects.get(pk=room_id, coworking_id=coworking_id, )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        agenda_rooms = AgendaRoom.objects.filter(room=room)
        serializer = AgendaRoomQuerySerializer(agenda_rooms, many=True)
        schedulings_to_send = {"schedulings": serializer.data}
        return Response(schedulings_to_send)


# coworkings/{oworking_id}/resource_schedulings/{resource_id}
class QueryResourceSchedulings(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, resource_id, format=None):
        try:
            resource = Resource.objects.get(pk=resource_id, coworking_id=coworking_id, )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        agenda_resources = AgendaResource.objects.filter(resource=resource)
        serializer = AgendaQueryResourceSerializer(agenda_resources, many=True)
        schedulings_to_send = {"schedulings": serializer.data}
        # schedulings_to_send["schedulings"] = serializer.data
        return Response(schedulings_to_send)


class QuerySchedulingsByYear(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, year):
        agendas = Agenda.objects.filter(date__year=year, coworking_id=coworking_id)
        serialized_agendas = QueryAgendaSerializer(agendas, many=True)

        return Response(data=serialized_agendas.data, status=status.HTTP_200_OK)


class QuerySchedulingsByMonth(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, year, month):
        agendas = Agenda.objects.filter(date__year=year, date__month=month, coworking_id=coworking_id)
        serialized_agendas = QueryAgendaSerializer(agendas, many=True)

        return Response(data=serialized_agendas.data, status=status.HTTP_200_OK)


class QuerySchedulingsByDay(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, year, month, day):
        agendas = Agenda.objects.filter(date__year=year, date__month=month, date__day=day, coworking_id=coworking_id)
        serialized_agendas = QueryAgendaSerializer(agendas, many=True)

        return Response(data=serialized_agendas.data, status=status.HTTP_200_OK)

        # coworkings/{oworking_id}/agenda_rooms


class QueryAllUserSchedulings(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, user_id):
        agendas = Agenda.objects.filter(coworking_id=coworking_id, user_plan__user_id=user_id)

        serializer_agendas = QueryAgendaSerializer(agendas, many=True)

        return Response(data={"schedulings": serializer_agendas.data}, status=status.HTTP_200_OK)

    def post(self, request, coworking_id, user_id):
        plan_id = request.data["plan"]

        try:
            user_plan = UserHasPlan.objects.get(plan_id=plan_id, user_id=user_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        agenda = QueryAgendaSerializer(request.data["scheduing"])

        if agenda.is_valid():
            return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(data=agenda.errors, status=status.HTTP_400_BAD_REQUEST)
