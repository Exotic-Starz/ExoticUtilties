from discord import *
from discord.ext import commands
import pyrebase
from discord.utils import get
from datetime import datetime, timedelta
import os
import re
import asyncio

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

pre = "!p "
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
admin = "admin"
leader = "leader"
moderator = "moderator"
traineeMod = "trainee mod"
cancel = ["cancel", "Cancel"]
skip = ["Skip", "skip"]
remove = ["Remove", "remove"]
stop = ["Stop", "stop"]

deny = "❎"
one = "1️⃣"
two = "2️⃣"
cancel_emoji = "⏹"


class Utility(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Utility is ready')

    @commands.command(aliases=["afk"])
    @commands.has_any_role("no life fan (level 80)")
    async def awayFromKeyboard(self, ctx, *, reason="AFK"):
        embed = Embed(description=f"**I set your AFK:** {reason}", color=random_color)
        await ctx.send(ctx.author.mention, embed=embed)

        if ctx.author.nick == None:
            db.child("AFK").child(ctx.author.id).update({"reason": reason})
            try:
                await ctx.author.edit(nick=f"[AFK]{ctx.author.name}")
            except:
                pass
        else:
            db.child("AFK").child(ctx.author.id).update({"reason": reason, "nick": ctx.author.nick})
            try:
                await ctx.author.edit(nick=f"[AFK]{ctx.author.nick}")
            except:
                pass
        return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:
            if message.guild == None:
                return
            isAFK = db.child("AFK").child(message.author.id).get().val()
            if isAFK != None:
                reason = "AFK"
                nickname = None
                for key, value in isAFK.items():
                    if key == "reason":
                        reason = value
                    elif key == "nick":
                        nickname = value

                embed = Embed(description=f"I have removed your AFK: {reason}", color=random_color)
                await message.channel.send(embed=embed)
                db.child("AFK").child(message.author.id).remove()
                if nickname != None:
                    try:
                        await message.author.edit(nick=nickname)
                    except:
                        pass
                else:
                    try:
                        await message.author.edit(nick=nickname)
                    except:
                        pass
            else:
                if message.mentions:
                    for mentioned in message.mentions:

                        reason = None
                        isAFK = db.child("AFK").child(mentioned.id).get().val()
                        if isAFK != None:
                            for key, value in isAFK.items():
                                if key == "reason":
                                    reason = value
                            embed = Embed(description=f"<@{mentioned.id}> is AFK: {reason}", color=random_color)
                            await message.channel.send(message.author.mention, embed=embed)\

    @commands.command()
    @commands.has_any_role(leader, moderator)
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)} ms")
        return
    @commands.command(aliases=["av"])
    @commands.has_any_role(leader, moderator)
    async def avatar(self, ctx, member: Member = None):
        if member is None:
            member = ctx.author

        embed = Embed(color=random_color)
        embed.set_author(name=member.name)
        embed.set_image(url=member.avatar_url)
        if member.id != ctx.author.id:
            embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)
        return

    @commands.command()
    async def membercount(self, ctx):
        bots = [bot for bot in ctx.guild.members if bot.bot is True]
        embed = Embed(title="Member Count", description=f"There are {len(ctx.guild.members)} members in **{ctx.guild.name}**\n**Humans:** {len(ctx.guild.members) - len(bots)}\n**Bots:** {len(bots)}",
                      color=random_color)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)
        return

    @commands.command()
    async def serverinfo(self, ctx):

        verificationLevel = ctx.guild.verification_level
        textChannelsCount = len(ctx.guild.text_channels)
        voiceChannelsCount = len(ctx.guild.voice_channels)
        guildRegion = ctx.guild.region
        roleCount = len(ctx.guild.roles)
        boostCount = ctx.guild.premium_subscription_count
        bootsTier = ctx.guild.premium_tier
        emojis = ctx.guild.emojis
        guildOwner = ctx.guild.get_member(ctx.guild.owner_id)
        animatedEmojis = 0
        createdAt = ctx.guild.created_at.strftime("%H:%M %p %B %d, %Y")
        for emoji in emojis:
            if emoji.animated:
                animatedEmojis += 1
        embed = Embed(title=f"General",
                      description=f"""**Name:** {ctx.guild.name}
**ID:** {ctx.guild.id}
**Owner:** {guildOwner} - {guildOwner.mention}
**Region:** {guildRegion}
**Boost Tier:** Tier {bootsTier}
**Verification Level:** {verificationLevel}
**Time Created:** {createdAt}""",
                      color=random_color)
        embed.add_field(name="Statics",
                        value=f"""**Role Count:** {roleCount}
**Emoji Count:** {len(emojis)}
**Regular Emoji Count:** {len(emojis) - animatedEmojis}
**Animated Emoji Count:** {animatedEmojis}
**Text Channels:** {textChannelsCount}
**Voice Channels:** {voiceChannelsCount}
**Boost Count:** {boostCount}""",
                        inline=False)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)
        return






def setup(client):
    client.add_cog(Utility(client))