import asyncio

import discord
from discord.ext import commands
from imdb import Cinemagoer
import requests # request img from web
import shutil # save img locally

class Act(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.ia = Cinemagoer()

    @commands.command(name="ActBio", aliases=["actbio",'Actbio','actBio'], usage = '(actor name)', help = "gives the bio of an actor")
    async def ActBio(self, ctx, *, name):
        aid = self.ia.search_person(name)[0].personID
        print("person ID recieved")
        person = self.ia.get_person(aid)

        text = person.get("mini biography")[0]
        lst = text.split('.')

        url = person.get("headshot")
        file_name = 'pic.jpg'
        res = requests.get(url, stream=True)

        await ctx.send("**" + person.get("name")+'**')

        if res.status_code == 200:
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(res.raw, f)
            with open(file_name, 'rb') as f:
                await ctx.send(file=discord.File(f))
        else:
            print("image download failed")

        while lst:
            ret =""
            ln = 0
            while lst and (ln+len(lst[0])) < 2000:
                ln = ln + len(lst[0]) + 2
                ret = ret+ lst.pop(0) + ". "
            #print(len(ret))
            await ctx.send(ret)

    @commands.command(name = 'actor', usage = "(actor name)", help="displays some basic information about an actor")
    async def actor(self,ctx,*,name):
        aid = self.ia.search_person(name)[0].personID
        print("person ID recieved")
        person = self.ia.get_person(aid)

        ret = person.get("birth date") +" "+person.get("birth notes")+"\n"
        if(person.get("nick names")):
           ret = ret+ ", ".join(person.get("nick names"))

        url = person.get("headshot")
        file_name = 'pic.jpg'
        res = requests.get(url, stream = True)

        await ctx.send("**"+ person.get("name")+"**")
        if res.status_code == 200:
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(res.raw, f)
            with open(file_name, 'rb') as f:
                await ctx.send(file=discord.File(f))
        else:
            print("image download failed")
        await ctx.send(ret)

    @commands.command(name = "filmog", usage="(actor name)", help= "provides the filmography of an actor")
    async def filmog(self,ctx,*, name):
        aid = self.ia.search_person(name)[0].personID
        print("person ID recieved")
        person = self.ia.get_person(aid)
        film = person.get("filmography").get("actor")

        ret = ""
        i = 0
        base = 10

        while i< base and i < len(film):
            ret = ret + str(film[i]) + " *as* " + str(film[i].currentRole) + '\n'
            i += 1

        msg = await ctx.send(ret)
        await msg.add_reaction("➡️")

        def check(reaction,user):
            return user == ctx.message.author and str(reaction.emoji) == '➡️'

        flag = True
        while flag and i<len(film):

            try:
                reaction, user = await self.client.wait_for('reaction_add',timeout=30.0, check = check)
            except asyncio.TimeoutError:
                await msg.clear_reaction("➡️")
                flag = False

            else:
                base = base+5
                ret =""
                while i < base and i < len(film):
                    ret = ret + str(film[i]) + " *as* " + str(film[i].currentRole) + '\n'
                    #await ctx.send(data['cast'][i])
                    i += 1
                msg = await ctx.send(ret)
                if i<len(film):
                    await msg.add_reaction("➡️")

    @commands.command(name = "wasin", usage="(actor name, movie name)", help = "checks to see if an actor was in a specific movie")
    async def wasin(self,ctx,*,request):
        req = request.split(", ")
        name = req[0]
        mov = req[1]

        aid = self.ia.search_person(name)[0].personID
        print("person ID recieved")
        person = self.ia.get_person(aid, info = ["filmography"])

        movie = self.ia.search_movie(mov)[0].movieID
        print("movie ID recieved")
        data = self.ia.get_movie(movie, info = ["main"])

        filmo = person.get("filmography").get("actor")
        i=0
        while i<len(filmo):
            if movie == filmo[i].getID():
                await ctx.send(str(person)+ " Played "+ str(filmo[i].currentRole) + ' in '+ str(data.get("title")))
                return
            i+=1
        await ctx.send(name + " did not play a role in "+ data.get("title"))

    @commands.command(name = "quotes", usage = "(actor name", help = "gets a number of quotes from an actor")
    async def quotes(self,ctx,*,name):
        aid = self.ia.search_person(name)[0].personID
        print("person ID recieved")
        person = self.ia.get_person(aid)

        ret = ''
        quotes = person.get("quotes")
        msg = await ctx.send("**"+person.get("name")+"**")
        i=0
        base =5
        while i<base and quotes:
            msg = await ctx.send("•"+quotes.pop(0).replace('[','*').replace(']',"*"))
            i+=1

        await msg.add_reaction("➡️")
        def check(reaction,user):
            return user == ctx.message.author and str(reaction.emoji) == '➡️'

        flag = True

        while flag and quotes:

            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await msg.clear_reaction("➡️")
                flag = False

            else:
                base = base + 5
                while i < base and quotes:
                    msg = await ctx.send("•"+quotes.pop(0).replace('[','*').replace(']',"*"))
                    i += 1
                if quotes:
                    await msg.add_reaction("➡️")
def setup(client):
    client.add_cog(Act(client))