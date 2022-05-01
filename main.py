import discord
import os
from discord.ext import commands
import json

if os.path.exists(os.getcwd()+"/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate={"Token":"","Prefix":"?"}
    with open(os.getcwd()+"/config.json", "w+")as f:
        json.dump(configTemplate,f)

token = configData["Token"]
prefix = configData["Prefix"]

vClient = commands.Bot(command_prefix=prefix)
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

vClient.run(token)
