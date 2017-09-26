# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView
from templated_docs import fill_template
from templated_docs.http import FileResponse

from ..serializers import *


class ContractDetail(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get(self, request, coworking_id, contract_id, format=None):
        try:
            contract = Contract.objects.get(pk=contract_id, coworking_id=coworking_id)
            # contract_serializer = Contra
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self):
        return

    def patch(self):
        return


class ContractList(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get(self, request, coworking_id, user_id, format=None):
        # try:
        contract = Contract.objects.get(user_id=user_id, coworking_id=coworking_id)
        contract_serializer = ContractSerializer(contract)
        contracts_to_send = {}
        contracts_to_send["contracts"] = contract_serializer.data
        # except ObjectDoesNotExist:
        return Response(contracts_to_send)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self):
        return


class BillDetail(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = Profile.objects.get(user_id=user_id)
        serialized_user = ProfileDocumentSerializer(user)

        print serialized_user.data

        doctype = 'pdf'
        filename = fill_template('privado.odt', serialized_user.data, output_format=doctype)
        visible_filename = 'teste.{}'.format(doctype)

        return FileResponse(filename, visible_filename)

    def delete(self):
        return
