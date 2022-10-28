from django.shortcuts import render
from django.db.models import F
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DiscordUser
from .serializers import DiscordUserSerializer


class User(APIView):
    def get(self, request, dcid, formate=None, **kwargs):
        user = DiscordUser.objects.get(discord_id=dcid)
        serializer = DiscordUserSerializer(user)
        return Response(serializer.data)


class UpdateExp(APIView):
    def post(self, request, formate=None):
        serializer = DiscordUserSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data['name']
            dcid = serializer.validated_data['discord_id']
            exp = serializer.validated_data['exp']

            if DiscordUser.objects.filter(discord_id=dcid).exists():
                serializer = DiscordUser.objects.get(discord_id=dcid)
                serializer.name = name
                serializer.exp = F('exp') + exp

            serializer.save()
            return Response(None, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubExp(APIView):
    def post(self, request, formate=None):
        serializer = DiscordUserSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data['name']
            dcid = serializer.validated_data['discord_id']
            exp = serializer.validated_data['exp']

            if DiscordUser.objects.filter(discord_id=dcid).exists():
                serializer = DiscordUser.objects.get(discord_id=dcid)
                serializer.name = name
                serializer.exp = F('exp') - exp

            serializer.save()
            return Response(None, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateLvl(APIView):
    def post(self, request, formate=None):
        serializer = DiscordUserSerializer(data=request.data)

        if serializer.is_valid():
            dcid = serializer.validated_data['discord_id']

            if DiscordUser.objects.filter(discord_id=dcid).exists():
                serializer = DiscordUser.objects.get(discord_id=dcid)
                serializer.lvl = F('lvl') + 1

            serializer.save()
            return Response(None, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RankingAPI(APIView):
    def get(self, request, formate=None, **kwargs):
        ranking = DiscordUser.objects.all().filter(is_active=True).order_by('-exp')[:25]
        serializer = DiscordUserSerializer(ranking, many=True)
        return Response(serializer.data)


class UserActive(APIView):
    def post(self, request):
        serializer = DiscordUserSerializer(data=request.data)

        if serializer.is_valid():
            dcid = serializer.validated_data['discord_id']

            if DiscordUser.objects.filter(discord_id=dcid).exists():
                serializer = DiscordUser.objects.get(discord_id=dcid)
                serializer.is_active = True

            serializer.save()
            return Response(None, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInactive(APIView):
    def post(self, request):
        serializer = DiscordUserSerializer(data=request.data)

        if serializer.is_valid():
            dcid = serializer.validated_data['discord_id']

            if DiscordUser.objects.filter(discord_id=dcid).exists():
                serializer = DiscordUser.objects.get(discord_id=dcid)
                serializer.is_active = False

            serializer.save()
            return Response(None, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
