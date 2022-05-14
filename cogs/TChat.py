import asyncio
import discord
from discord.ext import commands
from imdb import Cinemagoer
import requests # request img from web
import shutil # save img locally

class TChat(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.ia = Cinemagoer()

    @commands.command(name="data", usage ="(movie name)", help="displays a synopsis of the movie requested")
    async def data(self, ctx,*,name):
        movie = self.ia.search_movie(name)[0].movieID
        print("movie ID recieved")
        data = self.ia.get_movie(movie)
        ret = data['plot outline'][:2000]
        url = data['cover url']
        file_name = 'pic.jpg'
        res = requests.get(url, stream = True)
        await ctx.send(data["title"] +" ("+ str(data['year']) +')')
        if res.status_code == 200:
            with open(file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)
            with open(file_name,'rb') as f:
                await ctx.send(file=discord.File(f))
        else:
            print("image download failed")
        await ctx.send(ret)

    def proName(self,data):
        name = data.data['name'].replace('\n', "").split(" ")
        i = 0
        ret =''
        while i < 10 and i < len(name):
            if not name[i] == "" and not name[i].isnumeric():
                ret = ret+name[i] +" "
            i += 1
        ret = ret + " *as* "
        if(str(data.currentRole) != ""):
            ret = ret+str(data.currentRole)
        else:
            ret =  ret+"unknown"
        return ret + '\n'

    @commands.command(name = "cast", usage = "(movie name)", help = "List the cast of a movie in credits order")
    async def cast(self,ctx, *, name):
        movie = self.ia.search_movie(name)[0].movieID
        data = self.ia.get_movie(movie,info = ['full credits'])
        print("data recieved successfully")
        ret = ""
        ret = ret+name+" cast:\n"
        #await ctx.send(name+ " cast:")
        i = 0
        base = 10
        while i<base and i <len(data['cast']):
            ret = ret + self.proName(data['cast'][i])
            #await ctx.send(data['cast'][i])
            i+=1

        msg = await ctx.send(ret)
        await msg.add_reaction("➡️")

        def check(reaction,user):
            return user == ctx.message.author and str(reaction.emoji) == '➡️'

        flag = True

        while flag and i<len(data['cast']):

            try:
                reaction, user = await self.client.wait_for('reaction_add',timeout=30.0, check = check)
            except asyncio.TimeoutError:
                await msg.clear_reaction("➡️")
                flag = False

            else:
                base = base+5
                ret =""
                while i < base and i < len(data['cast']):
                    ret = ret + self.proName(data['cast'][i])
                    #await ctx.send(data['cast'][i])
                    i += 1
                msg = await ctx.send(ret)
                if i<len(data['cast']):
                    await msg.add_reaction("➡️")

    @commands.command(name = "crew",
                      usage="(movie name, role)",
                      help = "separate role and movie with a comma followed by a space\n"
                             "lists the credits of a given role from a specific movie\n"
                             "Role options include:\n"
                             "Director\n"
                             "Writer\n"
                             "Producer\n"
                             "Compser\n"
                             "Cinematographer\n"
                             "Editor\n"
                             "Casting Director\n"
                             "Production design\n"
                             "Production Manager\n"
                             "Art Department\n"
                             "Sound Crew\n"
                             "Visual Effects\n"
                             "Camera and Electrical Department\n"
                             "Animation Department\n"
                             "Casting Department\n"
                             "Editorial Department\n"
                             "Music Department\n"
                             "Script Department\n"
                             "Miscellaneous Crew\n"
                             "Thanks")
    async def crew(self,ctx,*, req):
        x = req.split(", ")
        name = x[0]
        role = x[1]
        print(x)
        movie = self.ia.search_movie(name)[0].movieID
        data = self.ia.get_movie(movie, info=['full credits'])
        await ctx.send(name + " " + role + ":")
        i = 0
        ret = set(data[role])
        print(ret)
        for i in ret:
            if i:
                await ctx.send(i)

def setup(client):
    client.add_cog(TChat(client))