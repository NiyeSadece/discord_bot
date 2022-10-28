from django.contrib import admin
from zoya.zoya_site.models import DiscordUser, ExcludedChannel, SpecialChannel


@admin.register(DiscordUser)
class DiscordUserAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'discord_id',
        'is_active',
        'exp',
        'lvl',
    ]


admin.site.register(ExcludedChannel)
admin.site.register(SpecialChannel)
