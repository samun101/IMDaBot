import discord
import os
from discord.ext import commands

vClient = commands.Bot(command_prefix="?")

@vClient.event
async def on_ready():
    print('We have logged in as {0.user}'.format(vClient))

inc_ext = []
for f in os.listdir('./cogs'):
    if f.endswith('.py'):
        inc_ext.append("cogs."+f[:-3])

if __name__ == '__main__':
    for ext in inc_ext:
        vClient.load_extension(ext)

vClient.run('OTYwNjM1NzM5NTUxNDU3MzEx.YktTwA.oBwD9eLcuzIW4UMdKCIIliyYXO0')
