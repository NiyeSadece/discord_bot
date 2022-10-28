import discord
import json
import requests
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from discord.ext.commands.errors import MemberNotFound
from zoya.local_settings import TOKEN


class Bot(commands.Bot):
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        await self.tree.sync(guild=discord.Object(id=534491377283629056))
        print(f"Synced slash command for {self.user}")

    async def on_command_error(self, ctx, error) -> None:
        await ctx.reply(error, ephemeral=True)


intents = discord.Intents.all()
client = Bot(command_prefix="==", intents=intents)


# todo: ogarnąć url i deployment
def update_exp(name, dcid, exp):
    url = 'http://127.0.0.1:8000/api/exp/update/'
    new_exp = {'name': name, 'discord_id': dcid, 'exp': exp}
    x = requests.post(url, data=new_exp)
    return


def sub_exp(name, dcid, exp):
    url = 'http://127.0.0.1:8000/api/exp/sub/'
    new_exp = {'name': name, 'discord_id': dcid, 'exp': exp}
    x = requests.post(url, data=new_exp)
    return


def update_lvl(dcid):
    url = 'http://127.0.0.1:8000/api/lvl/update/'
    new_lvl = {'discord_id': dcid}
    x = requests.post(url, data=new_lvl)
    return


def get_user(dsid):
    response = requests.get(f"http://127.0.0.1:8000/api/{dsid}/")
    json_data = json.loads(response.text)
    return json_data


def get_ranking():
    response = requests.get("http://127.0.0.1:8000/api/ranking/")
    json_data = json.loads(response.text)
    return json_data


def set_user_active(dcid):
    url = 'http://127.0.0.1:8000/api/user/active/'
    now_active = {'discord_id': dcid}
    x = requests.post(url, data=now_active)
    return


def set_user_inactive(dcid):
    url = 'http://127.0.0.1:8000/api/user/inactive/'
    now_inactive = {'discord_id': dcid}
    x = requests.post(url, data=now_inactive)
    return


def lvl_up(author_id):
    user = get_user(author_id)
    cur_xp = user["exp"]
    cur_lvl = user["lvl"]

    if cur_lvl < 4:
        if cur_xp > 80 * (2 ** cur_lvl):
            update_lvl(author_id)
            return True
        else:
            return False
    else:
        if cur_xp > 1200 + (300 * (cur_lvl - 4)):
            update_lvl(author_id)
            return True
        else:
            return False


# todo: change guild id
# showing level
@client.hybrid_command(name="lvl", with_app_command=True, description="Sprawdź poziom kreatywności", pass_context=True)
@app_commands.guilds(discord.Object(id=534491377283629056))
async def lvl(ctx: commands.Context, member: discord.Member = None):
    await ctx.defer()
    member = ctx.author if not member else member
    member_id = str(member.id)
    user = get_user(member_id)
    embed = discord.Embed(
        title='Creativity check!',
        description=f"{member.display_name}",
        colour=0xb180f9,
        timestamp=datetime.now()
    )
    embed.add_field(name="Poziom kreatywności:", value=user['lvl'])
    embed.add_field(name="Exp:", value=user['exp'])
    embed.set_author(name="Uniwersytet Obdarzonych", icon_url=str(ctx.guild.icon))
    embed.set_thumbnail(url=str(member.avatar))
    await ctx.send(embed=embed)


# showing ranking
@client.hybrid_command(name="rank", with_app_command=True, description="Sprawdź poziom kreatywności", pass_context=True)
@app_commands.guilds(discord.Object(id=534491377283629056))
async def rank(ctx: commands.Context):
    await ctx.defer()
    rank = 1
    embed = discord.Embed(
        title='Ranking kreatywności *Uniwersytetu Obdarzonych*',
        description="",
        colour=0xb180f9
    )
    ranking = get_ranking()
    for item in ranking:
        try:
            embed.add_field(name=f"{rank}.", value=f"<@{item['discord_id']}>")
            rank += 1
        except MemberNotFound:
            continue
    await ctx.send(embed=embed)


# manually adding exp
@client.command(pass_context=True)
@app_commands.guilds(discord.Object(id=534491377283629056))
async def addxp(ctx: commands.Context, xp, member: discord.Member = None):
    member = ctx.author if not member else member
    update_exp(member.display_name, member.id, xp)
    await ctx.send(f"Użytkownik {member} dostał {xp} punktów kreatywności!")

    if lvl_up(member.id):
        user = get_user(member.id)
        # channel_lvl = client.get_channel(909465395784736779)
        # await channel_lvl.send(
        #     f"No genialny jesteś {message.author.mention}, osiągnąłeś {user['lvl']} level, Ty kreatywna bestio! Oby tak dalej, a dostaniesz wspaniałe nagrody!")

# manually subtracting exp
@client.command(pass_context=True)
@app_commands.guilds(discord.Object(id=534491377283629056))
async def subxp(ctx: commands.Context, xp, member: discord.Member = None):
    member = ctx.author if not member else member
    sub_exp(member.display_name, member.id, xp)
    await ctx.send(f"Użytkownik {member} utracił {xp} punktów kreatywności!")


# setting user active, so they do show up in the ranking
@client.command(pass_context=True)
@app_commands.guilds(discord.Object(id=534491377283629056))
async def active(ctx: commands.Context, member: discord.Member = None):
    member = ctx.author if not member else member
    set_user_active(member.id)
    await ctx.send(f"Użytkownik {member} został ustawiony jako aktywny i będzie pokazywać się w rankingu!")


# setting user inactive, so they don't show up in the ranking
@client.command(pass_context=True)
@app_commands.guilds(discord.Object(id=534491377283629056))
async def inactive(ctx: commands.Context, member: discord.Member = None):
    member = ctx.author if not member else member
    set_user_inactive(member.id)
    await ctx.send(f"Użytkownik {member} został ustawiony jako nieaktywny i nie będzie pokazywać się w rankingu!")


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    #channel_log = client.get_channel(997155086029565953)
    #await channel_log.send("Zoya jest online!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.author.bot:
        # adding exp system
        # channel_log = client.get_channel(997155086029565953)
        msg = len(message.content)
        if msg > 499:
            msg_exp = msg // 100
            update_exp(message.author.display_name, message.author.id, msg_exp)
            # await channel_log.send(
            #     f"Dodano {msg_exp} exp {message.author.display_name} za odpis na <#{message.channel.id}>")

        if lvl_up(message.author.id):
            user = get_user(message.author.id)
            # channel_lvl = client.get_channel(909465395784736779)
            # await channel_lvl.send(
            #     f"No genialny jesteś {message.author.mention}, osiągnąłeś {user['lvl']} level, Ty kreatywna bestio! Oby tak dalej, a dostaniesz wspaniałe nagrody!")
    await client.process_commands(message)


client.run(TOKEN)
