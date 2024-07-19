import discord
from discord.ext import commands,tasks
from discord import app_commands
import os
from os import listdir
from dotenv import load_dotenv
from itertools import cycle

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)



@bot.event
async def on_ready():
		print(f'{bot.user.name} is online')
		change_status.start()
		await load_extensions()
		try:
			synced = await bot.tree.sync()
			print(f'Synced {len(synced)} command(s)')
		except Exception as e:
			print(e)

async def load_extensions():
    for cog in listdir('./cogs'):
    	if cog.endswith('.py') == True:
	    	await bot.load_extension(f'cogs.{cog[:-3]}')

statuslist = cycle([
		'Pondering the orb',
		'Watcthing you',
		'Living in your walls'
	])


@tasks.loop(seconds=16)
async def change_status():
	await bot.change_presence(activity=discord.Game(next(statuslist)))


load_dotenv()
TOKEN = os.getenv("token")
bot.run(TOKEN)