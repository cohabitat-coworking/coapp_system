# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import RequestFactory
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from coapp.serializers import *


class GetAllCoworkingsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)

        address = GenericAddress.objects.create(description="A fake address")
        Coworking.objects.create(name="Test coworking", address=address, cnpj="123456789012")
        Coworking.objects.create(name="Test coworking2", address=address, cnpj="123456789012")

    def test_get_all_coworkings(self):
        self.client.force_login(user=self.user)

        response = self.client.get('/api/coworkings', HTTP_AUTHORIZATION=self.token)

        coworkings = Coworking.objects.all()
        serialized_coworkings = CoworkingSerializer(coworkings, many=True)

        self.assertEqual(response.data, serialized_coworkings.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_coworkings_unnothorized(self):
        response = self.client.get('/api/coworkings')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetSingleCoworkingTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)

        address = GenericAddress.objects.create(description="A fake address")
        Coworking.objects.create(name="Test coworking", address=address, cnpj="123456789012")
        Coworking.objects.create(name="Test coworking2", address=address, cnpj="123456789012")

    def test_get_single_coworking(self):
        self.client.force_login(user=self.user)

        coworking = Coworking.objects.all()[0]
        coworking_id = coworking.id
        serialized_coworking = CoworkingSerializer(coworking)
        final_coworking = {"coworking": serialized_coworking.data}
        response = self.client.get('/api/coworkings/{}'.format(coworking_id), HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.data, final_coworking)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_coworking_not_found(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/coworkings/3', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_single_coworking_unauthorized(self):
        response = self.client.get('/api/coworkings/1')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateCoworkingTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)

        self.address = GenericAddress.objects.create(description="A fake address")

    def test_create_coworking(self):
        self.client.force_login(user=self.user)

        coworking = Coworking.objects.create(name="Test coworking", address=self.address, cnpj="123456789012")

        serialized_coworking = {"coworking": CoworkingCreationSerializer(coworking).data}

        response = self.client.post('/api/coworkings', serialized_coworking, HTTP_AUTHORIZATION=self.token,
                                    format='json')

        received_coworking = response.data["coworking"]
        serialized_received_coworking = CoworkingCreationSerializer(received_coworking)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(serialized_received_coworking)

    def test_create_coworking_bad_request_root_index(self):
        self.client.force_login(user=self.user)
        coworking = Coworking.objects.create(name="Test coworking", address_id=self.address.id,
                                             cnpj="123456789012")

        serialized_coworking = CoworkingCreationSerializer(coworking).data
        response = self.client.post('/api/coworkings', serialized_coworking, HTTP_AUTHORIZATION=self.token,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_coworking_bad_request_serializer(self):
        self.client.force_login(user=self.user)

        coworking = {"name": "Teste coworking", "cnpn": "123456789012"}

        response = self.client.post('/api/coworkings', coworking, HTTP_AUTHORIZATION=self.token,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteCoworkingTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)

        address = GenericAddress.objects.create(description="A fake address")
        Coworking.objects.create(name="Test coworking", address=address, cnpj="123456789012")

    def test_delete_coworking(self):
        self.client.force_login(user=self.user)
        coworking = Coworking.objects.all()[0]
        coworking_id = coworking.id

        response = self.client.delete('/api/coworkings/{}'.format(coworking_id), HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_coworking_not_found(self):
        self.client.force_login(user=self.user)
        response = self.client.delete('/api/coworkings/2', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EditCoworkingTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)

        address = GenericAddress.objects.create(description="A fake address")
        Coworking.objects.create(name="Test coworking", address=address, cnpj="123456789012")

    def test_patch_coworking(self):
        self.client.force_login(user=self.user)

        coworking = Coworking.objects.all()[0]
        coworking_id = coworking.id
        coworking.name = "New Name"
        coworking.cnpj = "111456189011"

        serialized_coworking = {"coworking": CoworkingCreationSerializer(coworking).data}

        response = self.client.patch('/api/coworkings/{}'.format(coworking_id), serialized_coworking,
                                     HTTP_AUTHORIZATION=self.token, format='json')

        update_coworking = Coworking.objects.get(pk=coworking_id)
        serialized_updated_coworking = {"coworking": CoworkingCreationSerializer(update_coworking).data}
        self.assertEqual(response.data, serialized_updated_coworking)
