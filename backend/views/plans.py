# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import *

# coworkings/{coworking_id}/plans
class PlanInfoList(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, format=None):
        plans = self.get_plans_in_coworking(coworking_id)
        serializers = PlanSerializer(plans, many=True)
        return Response(serializers.data)

    def get_plans_in_coworking(self, coworking_id):
        try:
            return Plan.objects.filter(coworking=coworking_id)
        except Plan.DoesNotExist:
            raise Http404

    def post(self, request, coworking_id, format=None):
        serializer = PlanCreationSerializer(data=request.data["plan"])
        plan = PlanSerializer(data=request.data["plan"])
        coworking = Coworking.objects.get(pk=coworking_id)

        if serializer.is_valid():
            try:
                if plan.is_valid():
                    plan_instance = plan.save(coworking=coworking)

                    for room_data in serializer.data["rooms"]:
                        room_instance = Room.objects.get(pk=room_data["room"])
                        plan_room = PlanRoom(plan=plan_instance,
                                             room=room_instance,
                                             quantity_hours=room_data["quantity_hours"])
                        plan_room.save()

                    for resource_data in serializer.data["resources"]:
                        resource_instance = Resource.objects.get(pk=resource_data["resource"])
                        plan_resource = PlanResource(plan=plan_instance,
                                                     resource=resource_instance,
                                                     quantity_hours=resource_data["quantity_hours"])
                        plan_resource.save()

                    for item_data in serializer.data["items"]:
                        item_instance = Item.objects.get(pk=item_data["item"])
                        plan_item = PlanItem(plan=plan_instance,
                                             item=item_instance,
                                             quantity=item_data["quantity"])
                        plan_item.save()

                    new_plan = {}
                    new_plan["plan"] = PlanDetailSerializer(plan_instance).data
                    return Response(new_plan, status=status.HTTP_201_CREATED)
            except:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


# coworkings/{coworking_id}/plans/{plan _id}
class PlanDetail(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, plan_id, format=None):
        plans = self.get_single_plan(coworking_id, plan_id)
        serializers = PlanDetailSerializer(plans.first(), many=False)
        return Response(serializers.data)

    def get_single_plan(self, coworking_id, plan_id):
        try:
            return Plan.objects.filter(coworking=coworking_id, id=plan_id)
        except Plan.DoesNotExist:
            raise Http404

    def delete(self, request, coworking_id, plan_id, format=None):
        try:
            plan = Plan.objects.get(pk=plan_id, coworking=coworking_id)
            plan.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, coworking_id, plan_id, format=None):
        try:
            plan = Plan.objects.get(pk=plan_id, coworking=coworking_id)
            serializer = PlanCreationSerializer(plan, data=request.data["plan"], partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

