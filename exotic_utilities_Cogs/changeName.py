from discord import *
from discord.ext import commands
import pyrebase
from discord.utils import get
from datetime import datetime, timedelta
import os
import re
import asyncio
from exotic_utilities_Cogs.Config.IDGenerator import IDGenerator
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
approve = "✅"


pre = "$"
t = True
f = False
usage = "**Usage :** "
explain = "**Explanation :** "
perms = "**Permissions :** "
aliases = "**Aliases :** "
example = "**Example :** "
cool_down = "**Cool Down :** "
note = "**Note :** "
another = "**or**"
head_staff = "Head Staff Φ"
leader = "leader"
moderator = "moderator"
traineeMod = "trainee mod"
cancel = ["cancel", "Cancel"]
skip = ["Skip", "skip"]
remove = ["Remove", "remove"]
stop = ["Stop", "stop"]
moderatorRoleID = 811107758023114753
leaderRoleID = 811001073602789386
deny = "❎"
one = "1️⃣"
two = "2️⃣"
cancel_emoji = "⏹"

class ChangeName(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('ChangeName is ready')
    @commands.command()
    @commands.has_any_role(leader, moderator)
    async def moderate(self, ctx, member: Member=None):
        if member is None:
            embed = Embed(title="How to use this command?",
                          description=f"`{prefix}moderate <@member>", color=random_color)
            await ctx.send(embed=embed)
            return
        else:
            if member.id == 788377671758905365:
                embed0 = Embed(description=f"Can't change the name of <@{member.id}> !", color=random_color)
                await ctx.send(embed=embed0)
                return
            else:

                ID = IDGenerator("nickname")
                newNick = f"Moderated Nickname {ID}"
                await member.edit(nick=newNick)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is False:
            if message.guild is None:
                return
            memberName = message.author.name
            memberNickName = message.author.nick or "None"

            bannedWords = db.child("automoderation").child(message.guild.id).get().val()
            if bannedWords is not None:
                changeName = False
                for key, value in bannedWords.items():
                    if key.lower() in memberName.lower() or key.lower() in memberNickName.lower():
                        changeName = True

                if changeName is False:
                    if message.author.id != 788377671758905365:
                        if "exotic starz" in memberName.lower() or "exotic starz" in memberNickName.lower():
                            changeName = True

                if changeName is True:
                    ID = IDGenerator("nickname")
                    newNick = f"Moderated Nickname {ID}"
                    await message.author.edit(nick=newNick)

def setup(client):
    client.add_cog(ChangeName(client))