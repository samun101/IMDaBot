import discord
from discord.ext import commands
from imdb import Cinemagoer
from youtubesearchpython.__future__ import VideosSearch
import asyncio

class Trailers(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.ia = Cinemagoer()

    @commands.command(name = "trailer")
    async def trailer(self, ctx,*, req):
        i=0
        Search = VideosSearch(req+" trailer", limit = 2)
        Result = await Search.next()
        msg = await ctx.send(Result['result'][0]['link'])
        await msg.add_reaction("➡️")

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == '➡️'

        flag = True

        while flag:

            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await msg.clear_reaction("➡️")
                flag = False

            else:
                Result = await Search.next()
                msg = await ctx.send(Result['result'][0]['link'])
                await msg.add_reaction("➡️")


def setup(client):
    client.add_cog(Trailers(client))