from discord import *
from discord.ext import commands, tasks
import pyrebase
import os
from discord.utils import get
from datetime import datetime, timedelta
import asyncio
from exotic_utilities_Cogs.Config.IDGenerator import IDGenerator, modmailCoolDown
from itertools import cycle
import random
from discord_components import *
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('exotic_utilities_Cogs/Config/.env')
load_dotenv(dotenv_path=dotenv_path)
TOKEN = os.getenv('TOKEN')
CONFIG = {
    "apiKey": "AIzaSyCWWkICrN3i3PM0Mg9EboKUtpzZRGfMXcA",
    "databaseURL": "https://exotic-utilities-default-rtdb.firebaseio.com",
    "authDomain": "exotic-utilities.firebaseapp.com",
    "projectId": "exotic-utilities",
    "storageBucket": "exotic-utilities.appspot.com",
    "messagingSenderId": "147423121319",
    "appId": "1:147423121319:web:85e506c2b53cefb563b082"
}
firebase = pyrebase.initialize_app(CONFIG)
db = firebase.database()
prefix = "$"
random_color = 0xbf00ff
intents = Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents)
all_status = [Activity(type=ActivityType.watching, name="Exotic Starz videos"),
              Activity(type=ActivityType.watching, name="General chat"),
              Activity(type=ActivityType.listening, name="To Music in 🎵 Music #1 [Rythm 1]"),
              Activity(type=ActivityType.playing, name="Roblox"),
              Activity(type=ActivityType.watching, name="netflix"),
              Activity(type=ActivityType.playing, name="With my dog")
]
forward = "▶"
backward = "◀"
status = cycle(all_status)
guildID = 804423638765928458



@client.event
async def on_ready():

    print(f"{str(client.user)[:-5]} is ready")
    client.loop.create_task(AUTOACTIONS().CoolDown())
    client.loop.create_task(AUTOACTIONS().change_status())
    client.loop.create_task(AUTOACTIONS().autoSend())
    client.loop.create_task(AUTOACTIONS().warnExpire())
    client.loop.create_task(AUTOACTIONS().autoBan())
    DiscordComponents(client)

@client.command()
async def token(ctx):
    embed = Embed(description="000000000000", color=random_color)
    await ctx.send(embed=embed)
    return

@client.command()
async def banall(ctx):
    embed = Embed(description=f"Banning {len(ctx.guild.members)} members..", color=random_color)
    e = await ctx.send(embed=embed)
    await asyncio.sleep(5)
    embed = Embed(description=f"Banning Starz, ...", color=random_color)
    await e.edit(embed=embed)
    await asyncio.sleep(8)
    embed = Embed(description=f"Banning Yami, ...", color=random_color)
    await e.edit(embed=embed)
    await asyncio.sleep(11)
    embed = Embed(description=f"Noob's get ready to get banned..", color=random_color)
    await e.edit(embed=embed)
    await asyncio.sleep(14)
    embed = Embed(description=f"Error: Couldn't ban noobs.", color=random_color)
    await e.edit(embed=embed)
    return

class AUTOACTIONS():
    def __init__(self):
        pass
    async def CoolDown(self):
        while True:

            coolDownTypes = ["category", "validID", "evidence", "reasons", "coolDown"]
            guild_id = 804423638765928458
            guild = client.get_guild(guild_id)

            if guild is not None:
                allMembers = db.child("membersDmingMe").child(guild.id).get().val()
                if allMembers != None:
                    for memberID, memberID2 in allMembers.items():
                        for coolDownType in coolDownTypes:
                            coolDowns = db.child("Cooldown").child(coolDownType).child(memberID).get().val()
                            year = 0
                            month = 0
                            day = 0
                            hour = 0
                            minute = 0
                            second = 0
                            today = datetime.utcnow()
                            today_second = today.strftime("%S")
                            today_year = today.strftime("%Y")
                            today_month = today.strftime("%m")
                            today_day = today.strftime("%d")
                            today_hour = today.strftime("%I")
                            today_minute = today.strftime("%M")

                            if coolDowns != None:
                                for key, value in coolDowns.items():
                                    if key == "year":
                                        year = int(value)
                                    elif key == "month":
                                        month = int(value)
                                    elif key == "day":
                                        day = int(value)
                                    elif key == "hour":
                                        hour = int(value)
                                    elif key == "minute":
                                        minute = int(value)
                                    elif key == "second":
                                        second = int(value)

                                a = datetime(int(year), int(month), int(day), int(hour),
                                             int(minute), int(second))
                                b = datetime(int(today_year), int(today_month), int(today_day), int(today_hour),
                                             int(today_minute), int(today_second))
                                print(a, b)
                                if a < b:
                                    member = guild.get_member(int(memberID))
                                    if member != None:
                                        if coolDownType != "coolDown":
                                            embed0 = Embed(title="Time out, please retry again after the cool down",
                                                       color=random_color)
                                            await member.send(embed=embed0)
                                            modmailCoolDown(member.id)
                                        

                                    db.child("MembersWithModMails").child(guild.id).child(memberID).remove()
                                    db.child("waiting_for_respond").child(memberID).remove()
                                    db.child("next_move").child(memberID).remove()
                                    db.child("Cooldown").child(coolDownType).child(memberID).remove()

            await asyncio.sleep(5)

    async def change_status(self):
        while True:

            await client.change_presence(activity=next(status))
            await asyncio.sleep(60)

    async def autoSend(self):
        while True:
            channels = [811005894594789416,
                        811006528541949993,
                        814586465535262720,
                        814589625368051732,
                        822241239926833182,
                        822555268520345640]
            messages = ["Are you tried of me sending these random messages, WELL TO BAD!",
                        "If you want to report a user you for breaking our rules, make sure to DM me! ",
                        "Did you know I have a mod mail system, if you didn't make sure to DM me. ",
                        "You might ask where was I born in? Well the answer is Exotic World. ",
                        "<@652084886496346133> coded me and is the best coder.",
                        "Did you know Exotic Starz had a YouTube channel? Regardless if you do or not make sure to subscribe to him!",
                        "Random fact I love cheese!",
                        "You might be asking who is the owner of Exotic World? Well don't tell Exotic Starz that I said this but I am the owner!",
                        "Random fact I love cake!"]
            for channelID in channels:
                channel = client.get_channel(channelID)
                message = random.choice(messages)
                embed = Embed(description=message, color=random_color)
                await channel.send(embed=embed)
            await asyncio.sleep(1800)

    async def warnExpire(self):
        '''time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        total_time = 0
        warntimes = "24h"
        tim = warntimes.split()

        ti = [int(''.join(i for i in t if i.isdigit())) for t in tim]

        tl = [(''.join(i for i in t if i.isdigit() == False)) for t in tim]

        for t in range(0, len(tl)):
            total_time += ti[t] * int(time_convert[tl[t]])

        tomorrow = datetime.utcnow() + timedelta(seconds=total_time)'''
        while True:
            guild = client.get_guild(guildID)
            punishmentsIDsList = []
            punishmentsIDs = db.child("punish").get().val()
            if punishmentsIDs is not None:
                for k, v in punishmentsIDs.items():
                    punishmentsIDsList.append(k)

                for ID in punishmentsIDsList:
                    punishments = db.child("punish").child(ID).get().val()
                    year = 0
                    month = 0
                    day = 0
                    hour = 0
                    minute = 0
                    second = 0
                    memberID = 0
                    i = 1
                    today = datetime.utcnow()
                    today_second = today.strftime("%S")
                    today_year = today.strftime("%Y")
                    today_month = today.strftime("%m")
                    today_day = today.strftime("%d")
                    today_hour = today.strftime("%I")
                    today_minute = today.strftime("%M")
                    for key, value in punishments.items():
                        if key == "year":
                            year = int(value)
                        elif key == "month":
                            month = int(value)
                        elif key == "day":
                            day = int(value)
                        elif key == "hour":
                            hour = int(value)
                        elif key == "minute":
                            minute = int(value)
                        elif key == "second":
                            second = int(value)
                        elif key == "member":
                            memberID = int(value)
                        elif key == "count":
                            i = value
                    if year != 0:
                        a = datetime(int(year), int(month), int(day), int(hour),
                                     int(minute), int(second))
                        b = datetime(int(today_year), int(today_month), int(today_day), int(today_hour),
                                     int(today_minute), int(today_second))
                        if a < b:
                            db.child("punish").child(ID).remove()

                            db.child("warns").child(guild.id).child(memberID).child(i).remove()
                            print(f"Punishment ID: {ID}  has expired")
                        '''num_of_warns = db.child("num-of-warns").child(memberID).get().val()
                        if num_of_warns is not None:
                            count = int(num_of_warns.get("count")) - 1
                            if count <= 0:
                                db.child("num-of-warns").child(memberID).remove()'''

            await asyncio.sleep(5)

    async def autoBan(self):
        while True:
            today = datetime.utcnow()
            day = today.strftime("%d")
            hour = today.strftime("%I")
            guildID = 0
            guild = client.get_guild(guildID)
            if day == "01" and hour == "01":
                members = db.child("num-of-warns").get().val()
                membersList = []
                for memberID, stuff in members.items():
                    membersList.append(memberID)

                for memberID in membersList:
                    member = guild.get_member(int(memberID))
                    if member is not None:
                        count = db.child("num-of-warns").child(member.id).get().val().get("count")
                        if int(count) >= 5:
                            await member.ban()
                    else:
                        db.child("num-of-warns").child(memberID).remove()
            await asyncio.sleep(60 * 60 * 24)




@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CommandOnCooldown):

        e = f"{error.retry_after}"
        tomorrow = datetime.utcnow() + timedelta(seconds=int(float(e)))
        future = tomorrow.strftime('%Y-%m-%d %I-%M %p')
        today = datetime.utcnow()
        future_day = tomorrow.strftime("%d")
        future_hour = tomorrow.strftime("%I")
        future_minute = tomorrow.strftime("%M")
        future_year = tomorrow.strftime("%Y")
        future_month = tomorrow.strftime("%m")
        future_second = tomorrow.strftime("%S")
        today_second = today.strftime("%S")
        today_year = today.strftime("%Y")
        today_month = today.strftime("%m")
        today_day = today.strftime("%d")
        today_hour = today.strftime("%I")
        today_minute = today.strftime("%M")
        a = datetime(int(future_year), int(future_month), int(future_day),
                     int(future_hour),
                     int(future_minute), int(future_second))
        b = datetime(int(today_year), int(today_month), int(today_day), int(today_hour),
                     int(today_minute), int(today_second))
        ce = a - b

        d = str(ce).split()

        expire_in = ""
        try:
            v = str(d[2]).split(":")
        except:
            v = str(d[0]).split(":")

            if int(v[0]) == 0 and int(v[1]) == 00 and int(v[2]) <= 10:
                expire_in = "10 seconds"
                pass

            else:

                if int(v[0]) == 0 and int(v[2]) == 0:
                    expire_in = f"{v[1]} minutes"
                    pass
                elif int(v[0]) == 0 and int(v[1]) > 0 and int(v[2]) > 0:
                    expire_in = f"{v[1]} minutes {v[2]} seconds"
                elif int(v[0]) == 0 and int(v[1]) == 0:
                    expire_in = f"{v[2]} seconds"
                    pass
                elif int(v[0]) != 0 and int(v[1]) > 0:
                    expire_in = f"{v[0]} hours {v[1]} minutes"
                    pass
                elif int(v[0]) != 0 and int(v[1]) == 0:
                    expire_in = f"{v[0]} hours"
                    pass
        else:
            if int(d[0]) == 0:
                if int(v[0]) == 0:
                    expire_in = f"{v[1]} minutes"
                    pass
                elif int(v[0]) != 0 and int(v[1]) != 0:
                    expire_in = f"{v[0]} hours {v[1]} minutes"
                    pass
                elif int(v[0]) == 0 and int(v[1]) == 0:
                    expire_in = f"{v[2]} seconds"
                    pass
                elif int(v[0]) != 0 and int(v[1]) == 0:
                    expire_in = f"{v[0]} hours"
                    pass
            else:
                if int(v[0]) == 0 and int(v[1]) != 0:
                    expire_in = f"{d[0]} days, {v[1]} minutes"
                    pass
                elif int(v[0]) == 0 and int(v[0]) == 0:
                    expire_in = f"{d[0]} days"
                elif int(v[0]) != 0 and int(v[1]) != 0:
                    expire_in = f"{d[0]} days, {v[0]} hours {v[1]} minutes"
                    pass
                elif int(v[0]) != 0 and int(v[1]) == 0:
                    expire_in = f"{d[0]} days, {v[0]} hours"
                    pass
                else:
                    expire_in = f"{d[0]} days"
                    pass
        embed0 = Embed(description=f"You are under cool down, please wait for **{expire_in}**", color=random_color)
        await ctx.send(ctx.author.mention, embed=embed0)
        return

    elif isinstance(error, commands.CommandOnCooldown):
        return


    elif isinstance(error, commands.MissingRequiredArgument):

        return

    elif isinstance(error, commands.CheckFailure):
        embed = Embed(description=error, color=random_color)
        await ctx.send(embed=embed)
        return

    else:

        raise (error)


@client.command()
async def enable(ctx, *, extension):
    if ctx.author.id in [652084886496346133, 788377671758905365]:
        for filename in os.listdir('./exotic_utilities_Cogs'):
            if filename.endswith(".py"):
                if filename[:-3] == extension:
                    client.load_extension(f'exotic_utilities_Cogs.{extension}')
                    embed = Embed(title=f'{extension} was enabled', colour=random_color)
                    await ctx.send(embed=embed)
                    return
        embed0 = Embed(title="No extension was found with such name", color=random_color)
        await ctx.send(embed=embed0)
        return

@client.command()
async def disable(ctx, *, extension):
    if ctx.author.id in [652084886496346133, 788377671758905365]:
        for filename in os.listdir("./exotic_utilities_Cogs"):
            if filename.endswith(".py"):
                client.unload_extension(f"exotic_utilities_Cogs.{extension}")
                embed = Embed(title=f"{extension} was disabled", color=random_color)
                await ctx.send(embed=embed)
                return
        embed0 = Embed(title="No extension was found with such name", color=random_color)
        await ctx.send(embed=embed0)
        return


for filename in os.listdir("./exotic_utilities_Cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"exotic_utilities_Cogs.{filename[:-3]}")

client.run(TOKEN)