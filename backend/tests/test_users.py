# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import RequestFactory
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from backend.serializers import *


class GetAllUsersTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        address = GenericAddress.objects.create(description="A fake address")
        self.coworking = Coworking.objects.create(name="Test coworking", address=address, cnpj="123456789012")

        self.user1 = User.objects.create_user('test_user_personal', 'usertestpersonal@gmail.com', 'test1234')
        self.user2 = User.objects.create_user('test_user_juridic', 'usertestjuridic@gmail.com', 'test1234')

        Profile.objects.create(user=self.user1, cpf="12345678901", rg="111222333444", coworking=self.coworking)
        ProfileJuridic.objects.create(user=self.user2, cnpj="12121212", juridic_name="Aname",
                                      fantasy_name="anothername", coworking=self.coworking)

    def test_get_all_users(self):
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)

        self.client.force_login(user=self.user)
        response = self.client.get('/api/v1/coworkings/{}/users'.format(self.coworking.id),
                                   HTTP_AUTHORIZATION=self.token)

        personal_users = Profile.objects.filter(coworking=self.coworking)
        juridic_users = ProfileJuridic.objects.filter(coworking=self.coworking)

        serialized_personal_profiles = ProfileSerializer(personal_users, many=True)
        serialized_juridic_profiles = JuridicProfileSerializer(juridic_users, many=True)
        final_response = {"users": {
            "personal": serialized_personal_profiles.data,
            "juridic": serialized_juridic_profiles.data
        }
        }

        self.assertEqual(final_response, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_single_user(self):
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)

        self.client.force_login(user=self.user)
        response = self.client.get('/api/v1/coworkings/{}/users/{}'.format(self.coworking.id, self.user1.id),
                                   HTTP_AUTHORIZATION=self.token)

        try:
            user = Profile.objects.get(user=self.user1)
        except:
            user = ProfileJuridic.objects.get(user=self.user1)
