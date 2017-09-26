# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import RequestFactory
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from backend.serializers import *


class GetAllContactsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)

        address = GenericAddress.objects.create(description="A fake address")
        self.coworking = Coworking.objects.create(name="Test coworking", address=address, cnpj="123456789012")
        contact_type = ContactType.objects.create(coworking=self.coworking, type="type_test")
        ContactType.objects.create(coworking=self.coworking, type="type_test2")

        ContactInfo.objects.create(coworking=self.coworking, name="A contact info", info="testtest", type=contact_type)
        ContactInfo.objects.create(coworking=self.coworking, name="Another contact info", info="test2test2",
                                   type=contact_type)

    def test_get_all_contacts(self):
        self.client.force_login(user=self.user)

        response = self.client.get('/api/v1/coworkings/{}/contact_infos'.format(self.coworking.id),
                                   HTTP_AUTHORIZATION=self.token)

        contact_infos = ContactInfo.objects.filter(coworking=self.coworking)

        serialized_contact_infos = {"contact_infos": ContactInfoSerializer(contact_infos, many=True).data}

        self.assertEqual(serialized_contact_infos, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_contact_types(self):
        self.client.force_login(user=self.user)

        response = self.client.get('/api/v1/coworkings/{}/contact_types'.format(self.coworking.id),
                                   HTTP_AUTHORIZATION=self.token)

        contact_types = ContactType.objects.filter(coworking=self.coworking)

        serialized_contact_types = {"contact_types": ContactTypeSerializer(contact_types, many=True).data}

        self.assertEqual(serialized_contact_types, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_contacts_info_not_found_coworking(self):
        self.client.force_login(user=self.user)

        response = self.client.get(
            '/api/v1/coworkings/{}/contact_infos'.format(2),
            HTTP_AUTHORIZATION=self.token)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class CreateContactInfoTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)

        address = GenericAddress.objects.create(description="A fake address")
        self.coworking = Coworking.objects.create(name="Test coworking", address=address, cnpj="123456789012")

    def test_create_contact_info(self):
        self.client.force_login(user=self.user)

        contact_type = ContactType.objects.create(coworking=self.coworking, type="type_test")
        contact_info = ContactInfo.objects.create(coworking=self.coworking, name="A contact info", info="testtest",
                                                  type=contact_type)

        serialized_contact = {"contact_info": ContactInfoCreationSerializer(contact_info).data}

        response = self.client.post('/api/v1/coworkings/{}/contact_infos'.format(self.coworking.id), serialized_contact,
                                    HTTP_AUTHORIZATION=self.token,
                                    format='json')

        received_contact = response.data["contact_info"]
        serialized_received_contact = ContactInfoSerializer(received_contact)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(serialized_received_contact)

    def test_create_contact_info_bad_request_serializer(self):
        self.client.force_login(user=self.user)

        contact_type = ContactType.objects.create(coworking=self.coworking, type="type_test")
        contact_info = ContactInfo.objects.create(coworking=self.coworking, name="A contact info", info="testtest",
                                                  type=contact_type)

        serialized_contact = {"contact_info": ContactInfoSerializer(contact_info).data}

        response = self.client.post('/api/v1/coworkings/{}/contact_infos'.format(self.coworking.id), serialized_contact,
                                    HTTP_AUTHORIZATION=self.token,
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_info_bad_request_structure(self):
        self.client.force_login(user=self.user)

        contact_type = ContactType.objects.create(coworking=self.coworking, type="type_test")
        contact_info = ContactInfo.objects.create(coworking=self.coworking, name="A contact info", info="testtest",
                                                  type=contact_type)

        contact_info_json = {"coworking": CoworkingSerializer(self.coworking).data, "nome": "A Name"}
        serialized_contact = {"cotact_info": contact_info_json}

        response = self.client.post('/api/v1/coworkings/{}/contact_infos'.format(self.coworking.id), serialized_contact,
                                    HTTP_AUTHORIZATION=self.token,
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_info_not_found_coworking(self):
        self.client.force_login(user=self.user)

        contact_type = ContactType.objects.create(coworking=self.coworking, type="type_test")
        contact_info = ContactInfo.objects.create(coworking=self.coworking, name="A contact info", info="testtest",
                                                  type=contact_type)

        serialized_contact = {"contact_info": ContactInfoCreationSerializer(contact_info).data}

        response = self.client.post('/api/v1/coworkings/{}/contact_infos'.format(2), serialized_contact,
                                    HTTP_AUTHORIZATION=self.token,
                                    format='json')

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class GetSingleContactTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)

        address = GenericAddress.objects.create(description="A fake address")
        self.coworking = Coworking.objects.create(name="Test coworking", address=address, cnpj="123456789012")
        contact_type = ContactType.objects.create(coworking=self.coworking, type="type_test")
        ContactType.objects.create(coworking=self.coworking, type="type_test2")

        self.contact_info = ContactInfo.objects.create(coworking=self.coworking, name="A contact info", info="testtest",
                                                       type=contact_type)

    def test_get_single_contact_info(self):
        self.client.force_login(user=self.user)

        response = self.client.get(
            '/api/v1/coworkings/{}/contact_infos/{}'.format(self.coworking.id, self.contact_info.id),
            HTTP_AUTHORIZATION=self.token)

        contact_info = ContactInfo.objects.get(pk=self.contact_info.id)

        serialized_contact = {"contact_info": ContactInfoSerializer(contact_info).data}

        self.assertEqual(serialized_contact, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_contact_info_not_found_contact(self):
        self.client.force_login(user=self.user)

        response = self.client.get(
            '/api/v1/coworkings/{}/contact_infos/{}'.format(self.coworking.id, 2),
            HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_contact_info_not_found_coworking(self):
        self.client.force_login(user=self.user)

        response = self.client.get(
            '/api/v1/coworkings/{}/contact_infos/{}'.format(2, self.contact_info.id),
            HTTP_AUTHORIZATION=self.token)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class DeleteContactTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)

        address = GenericAddress.objects.create(description="A fake address")
        self.coworking = Coworking.objects.create(name="Test coworking", address=address, cnpj="123456789012")
        contact_type = ContactType.objects.create(coworking=self.coworking, type="type_test")
        ContactType.objects.create(coworking=self.coworking, type="type_test2")

        self.contact_info = ContactInfo.objects.create(coworking=self.coworking, name="A contact info", info="testtest",
                                                       type=contact_type)

    def test_delete_single_contact_info(self):
        self.client.force_login(user=self.user)

        response = self.client.delete(
            '/api/v1/coworkings/{}/contact_infos/{}'.format(self.coworking.id, self.contact_info.id),
            HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_contact_info_not_found_contact(self):
        self.client.force_login(user=self.user)

        response = self.client.delete(
            '/api/v1/coworkings/{}/contact_infos/{}'.format(self.coworking.id, 2),
            HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_contact_info_not_found_coworking(self):
        self.client.force_login(user=self.user)

        response = self.client.delete(
            '/api/v1/coworkings/{}/contact_infos/{}'.format(2, self.contact_info.id),
            HTTP_AUTHORIZATION=self.token)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class UpdateContactTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)

        address = GenericAddress.objects.create(description="A fake address")
        self.coworking = Coworking.objects.create(name="Test coworking", address=address, cnpj="123456789012")
        contact_type = ContactType.objects.create(coworking=self.coworking, type="type_test")
        ContactType.objects.create(coworking=self.coworking, type="type_test2")

        self.contact_info = ContactInfo.objects.create(coworking=self.coworking, name="A contact info", info="testtest",
                                                       type=contact_type)

    def test_patch_contact_info(self):
        self.client.force_login(user=self.user)

        self.contact_info.name = "changed name"

        serialized_edited = {"contact_info": ContactInfoCreationSerializer(self.contact_info).data}

        response = self.client.patch(
            '/api/v1/coworkings/{}/contact_infos/{}'.format(self.coworking.id, self.contact_info.id), serialized_edited,
            HTTP_AUTHORIZATION=self.token, format='json')

        update_contact = ContactInfo.objects.get(pk=self.contact_info.id)
        serialized_updated_contact_info = {"contact_info": ContactInfoCreationSerializer(update_contact).data}
        self.assertEqual(response.data, serialized_updated_contact_info)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_bad_request_serializer(self):
        self.client.force_login(user=self.user)

        self.contact_info.name = "changed name"

        serialized_edited = {"contact_info": ContactInfoSerializer(self.contact_info).data}

        response = self.client.patch(
            '/api/v1/coworkings/{}/contact_infos/{}'.format(self.coworking.id, self.contact_info.id), serialized_edited,
            HTTP_AUTHORIZATION=self.token, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_bad_request_structure(self):
        self.client.force_login(user=self.user)

        self.contact_info.name = "changed name"

        serialized_edited = {"contct_nfo": ContactInfoSerializer(self.contact_info).data}

        response = self.client.patch(
            '/api/v1/coworkings/{}/contact_infos/{}'.format(self.coworking.id, self.contact_info.id), serialized_edited,
            HTTP_AUTHORIZATION=self.token, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_not_found_coworking(self):
        self.client.force_login(user=self.user)

        self.contact_info.name = "changed name"

        serialized_edited = {"contact_info": ContactInfoCreationSerializer(self.contact_info).data}

        response = self.client.patch(
            '/api/v1/coworkings/{}/contact_infos/{}'.format(2, self.contact_info.id), serialized_edited,
            HTTP_AUTHORIZATION=self.token, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_not_found_info(self):
        self.client.force_login(user=self.user)

        self.contact_info.name = "changed name"

        serialized_edited = {"contact_info": ContactInfoCreationSerializer(self.contact_info).data}

        response = self.client.patch(
            '/api/v1/coworkings/{}/contact_infos/{}'.format(self.coworking.id, 2), serialized_edited,
            HTTP_AUTHORIZATION=self.token, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
