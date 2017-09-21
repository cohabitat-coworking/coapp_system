# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import *


# users/sign_in
class UserSignIn(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, IsAuthenticated]

    def post(self, request):
        content = request.data["user"]

        username = content["username"]
        password = content["password"]

        if username and password:
            user = authenticate(username=username, password=password)

            if user is not None:

                token = Token.objects.get(user=user)

                serialized_token = UserToken(token)

                return Response(data=serialized_token.data, status=status.HTTP_200_OK)
            else:
                return Response(data=None, status=status.HTTP_404_NOT_FOUND)


class UserList(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get(self, request, coworking_id):
        users_personal = Profile.objects.filter(coworking_id=coworking_id)
        users_juridic = ProfileJuridic.objects.filter(coworking_id=coworking_id)

        all_users = {}
        all_users["personal"] = ProfileSerializer(users_personal, many=True).data
        all_users["juridic"] = JuridicProfileSerializer(users_juridic, many=True).data

        final_wrapper = {"users": all_users}

        return Response(data=final_wrapper, status=status.HTTP_200_OK)

    def post(self, request, coworking_id):

        content = json.loads(request.body)
        type = content["profile"]["type"]
        del content["profile"]["type"]

        if type == "personal":
            serialized_profile = PersonalProfileCreationSerializer(data=content["profile"])
            if serialized_profile.is_valid():
                profile = serialized_profile.data

                new_user = User.objects.create(
                    username=profile['user']['username'],
                    email=profile['user']['email'],
                    first_name=profile['user']['first_name'],
                    last_name=profile['user']['last_name']
                )
                new_user.set_password(profile['user']['password'])
                new_user.save()
                Token.objects.create(user=new_user)

                coworking = Coworking.objects.get(pk=coworking_id)
                new_profile = Profile.objects.create(
                    user=new_user,
                    cpf=profile['cpf'],
                    rg=profile['rg'],
                    coworking=coworking,
                    address_id=profile['address']
                )

                token_serialized = {"user": ProfileSerializer(new_profile).data}

                return Response(data=token_serialized, status=status.HTTP_200_OK)
            else:
                return Response(data=serialized_profile.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serialized_profile = JuridicProfileCreationSerializer(data=content["profile"])
            if serialized_profile.is_valid():
                profile = serialized_profile.data

                new_user = User.objects.create(
                    username=profile['user']['username'],
                    email=profile['user']['email'],
                    first_name=profile['user']['first_name'],
                    last_name=profile['user']['last_name']
                )
                new_user.set_password(profile['user']['password'])
                new_user.save()
                Token.objects.create(user=new_user)

                coworking = Coworking.objects.get(pk=coworking_id)
                new_profile = ProfileJuridic.objects.create(
                    user=new_user,
                    cnpj=profile['cnpj'],
                    address_id=profile['address'],
                    coworking=coworking
                )

                token_serialized = {"user": JuridicProfileSerializer(new_profile).data}

                return Response(data=token_serialized, status=status.HTTP_200_OK)
            else:
                return Response(data=serialized_profile.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, coworking_id, user_id):

        user = User.objects.get(pk=user_id)
        try:
            profile = Profile.objects.get(coworking_id=coworking_id, user=user)
            serialized_profile = ProfileSerializer(profile)
            profile_to_send = {"profile": serialized_profile.data}
            profile_to_send["type"] = "personal"
            return Response(data=profile_to_send, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            profile = ProfileJuridic.objects.get(coworking_id=coworking_id, user=user)
            serialized_profile = JuridicProfileSerializer(profile)
            profile_to_send = {"profile": serialized_profile.data}
            profile_to_send["type"] = "juridic"
            return Response(data=profile_to_send, status=status.HTTP_200_OK)

    def patch(self):
        return

    def delete(self, request, coworking_id, user_id):

        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


# coworkings/{coworking_id}/users/{user_id}/images
class PersonalUserImageUpload(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, coworking_id, user_id, format=None):
        try:
            profile = Profile.objects.get(user_id=user_id, coworking_id=coworking_id)
            image_to_upload = request.data['image']

            profile.profile_image = image_to_upload

            timestr = str(datetime.now())
            profile.profile_image.name = timestr + "-" + profile.profile_image.name
            profile.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
