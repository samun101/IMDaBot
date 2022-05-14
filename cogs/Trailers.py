import discord
from discord.ext import commands
import youtube_dl
from imdb import Cinemagoer
from youtubesearchpython.__future__ import VideosSearch
import asyncio
from discord.utils import get
import os

class Trailers(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.ia = Cinemagoer()
        self.Search = ""
        self.url = ""

    @commands.command(name = "trailer")
    async def trailer(self, ctx,*, req):
        i=0
        self.Search = VideosSearch(req+" trailer", limit = 2)
        Result = await self.Search.next()
        self.url = Result['result'][0]['link']
        msg = await ctx.send(self.url)
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
                Result = await self.Search.next()
                msg = await ctx.send(Result['result'][0]['link'])
                await msg.add_reaction("➡️")

    @commands.command(name='join')
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send(ctx.message.author.name + " not in channel")
            return
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

    async def trailr(self, req):
        i=0
        self.Search = VideosSearch(req+" trailer", limit = 2)
        Result = await self.Search.next()
        self.url = Result['result'][0]['link']

    @commands.command(name='play')
    async def play(self, ctx,*, trail):
        song_there = os.path.isfile('song.mp3')
        voice = get(self.client.voice_clients, guild=ctx.guild)
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("wait for current trailer to end or use the stop command")
            return
        print(youtube_dl)
        await self.trailr(trail)
        await ctx.send(self.url)
        ydl_opts = {'format': 'bestaudio', 'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            os.system("youtube-dl --rm-cache-dir")
            stream = os.popen('echo Returned output')
            output = stream.read()
            print(output)
            ydl.download([self.url])
        for file in os.listdir('./'):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio('song.mp3'))

    @commands.command(name='next')
    async def next(self, ctx):
        song_there = os.path.isfile('song.mp3')
        voice = get(self.client.voice_clients, guild=ctx.guild)
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("wait for current trailer to end or use the stop command")
            return
        print(youtube_dl)
        result = await self.Search.next()
        self.url = result['result'][0]['link']
        await ctx.send(self.url)
        ydl_opts = {'format': 'bestaudio', 'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            os.system("youtube-dl --rm-cache-dir")
            stream = os.popen('echo Returned output')
            output = stream.read()
            print(output)
            ydl.download([self.url])
        for file in os.listdir('./'):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio('song.mp3'))

    @commands.command(name='stop', help='Stops the trailer')
    async def stop(self, ctx):
        voice_client = get(self.client.voice_clients, guild=ctx.guild)
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='leave')
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")


def setup(client):
    client.add_cog(Trailers(client))