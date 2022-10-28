from rest_framework import serializers
from .models import DiscordUser


class DiscordUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscordUser
        fields = [
            'name',
            'discord_id',
            'is_active',
            'exp',
            'lvl',
        ]
        extra_kwargs = {'name': {'required': False}}

