# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from backend.models import *


# Create your tests here.

class ProfileTest(TestCase):
    def setUp(self):
        address = GenericAddress.objects.create(description="A fake address")

        coworking = Coworking.objects.create(name="Test coworking", address=address, cnpj="123456789012")

        user_address = UserAddress.objects.create(description="A fake address")

        user = User.objects.create(username="levima", email="levi@mail.com")
        user.set_password("levi1110")

        Profile.objects.create(user=user, cpf="04454653364", rg="2005007077851", coworking=coworking,
                               address=user_address)

    def test_profile_cpf(self):
        user = User.objects.get(username="levima")
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.get_cpf(), "04454653364")
