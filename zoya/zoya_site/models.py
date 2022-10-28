from django.db import models


class DiscordUser(models.Model):
    name = models.CharField(max_length=125)
    discord_id = models.IntegerField()
    is_active = models.BooleanField(default=True)
    exp = models.IntegerField(default=0)
    lvl = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class ExcludedChannel (models.Model):
    name = models.CharField(max_length=125)
    discord_id = models.IntegerField()

    def __str__(self):
        return self.name


class SpecialChannel (ExcludedChannel):
    LOG = "log"
    MESSAGE = "msg"
    CHANNEL_TYPE = [
        (LOG, "log channel"),
        (MESSAGE, "message channel"),
    ]
    type = models.CharField(max_length=3, choices=CHANNEL_TYPE)

    def __str__(self):
        return self.name
