import discord
from discord import ctx
import asyncio
import ServerSideWork
import json
from concurrent.futures import ThreadPoolExecutor
#TODO: Update Usernames the first time they interact with the bot after changign the usernames
with open('BOTInfo.json', 'r') as JsonHold:
  __jsonData = json.load(JsonHold)
botName = __jsonData["botName"]
guild = __jsonData['guild']
__token = __jsonData['token']
__jsonData = None
intents = discord.Intents.all()
client = discord.Client(intents=intents)
channel = discord.guild.ChannelType.text
server = None
ssw = ServerSideWork.ServerWork()

@client.event
async def on_ready():
  """
  This function is called when the bot is ready to interact with discord.
  """
  global server, guild, channel
  print("Logged in as")
  print(botName)
  print(client.user.id)
  print("------")
  server = discord.utils.get(client.guilds, name=guild)
  for i in server.text_channels:
    if i.name == "bot-commands":
      channel = i
  print("Logging to Channel bot-commands on " + server.name)
@client.event
async def on_message(message):
  """
  This function is called when a message is sent in the discord server.
  """
  if message.channel == channel and message.author!= client.user and message.content.startswith("!"):
    await parser(message)
    
async def parser(message):
  """
  This function is called when a message is sent in the discord server AND is a command for the bot to interpret
  """
  global ssw
  command = message.content.split(" ")[0][1:]
  parameters = message.content.split(" ")[1:]
  pool = ThreadPoolExecutor()
  await asyncio.get_event_loop().run_in_executor(pool,ssw.addUser,message,parameters)
  if command == "addchar":
    await asyncio.get_event_loop().run_in_executor(pool,ssw.addChar,message,parameters)
  elif command == "delchar":
    await asyncio.get_event_loop().run_in_executor(pool,ssw.delChar,message,parameters)
  elif command == "char":
    await asyncio.get_event_loop().run_in_executor(pool,ssw.getChar,message,parameters)
  elif command == "list":
    await asyncio.get_event_loop().run_in_executor(pool,ssw.list,message,parameters)
  elif command == "help":
    await asyncio.get_event_loop().run_in_executor(pool,ssw.help,message,parameters)
  
    
@client.event
async def op():
  """
  This function is called when the bot is ready to interact with discord.
  """
  global channel, ssw
  pool = ThreadPoolExecutor()
  while True:
    i = await asyncio.get_event_loop().run_in_executor(pool,ssw.getOutput)
    if i!= '':
      await channel.send(i)
    await asyncio.sleep(.5)
    
# Define the main() coroutine that will run your bot 
async def main(token):
  # Log in the client
  await client.login(token)
  # Get the channel where you want to send messages
  # Start the op() coroutine concurrently with the client
  await asyncio.gather(client.start(token), op())
  asyncio.wait()
# Use asyncio.run() to run the main() coroutine
asyncio.run(main(__token))