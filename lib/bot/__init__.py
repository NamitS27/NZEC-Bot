from discord import Intents
from glob import glob
import datetime
from math import *
from asyncio import sleep
import discord
from discord.ext.commands import Bot as BotBase
from discord import Embed,File
from discord.ext.commands import Context
from discord.errors import Forbidden
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,CommandOnCooldown)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

PREFIX = "~"
COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f" {cog} cog is now ready!")

	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.cogs_ready = Ready()
		self.scheduler = AsyncIOScheduler()
		super().__init__(command_prefix=PREFIX,intents=Intents.all())

	def pretty_print_time(self,seconds: int):
		days, seconds = divmod(seconds, 86400)
		hours, seconds = divmod(seconds, 3600)
		minutes, seconds = divmod(seconds, 60)
		if days>0:
			return f"{days} days, {hours} hours {minutes} mins and {seconds} secs"
		elif hours>0:
			return f"{hours} hours {minutes} mins and {seconds} secs"
		elif minutes>0:
			return f"{minutes} mins and {seconds} secs"
		else:
			return f"{seconds} secs"

	def setup(self):
		print(" COGS =",COGS)
		for cog in COGS:
			self.load_extension(f"lib.cogs.{cog}")
			print(f" {cog} cog is lock and loaded")

		print("setup complete")

	def run(self):
		print("Running setup...")
		self.setup()
		self.TOKEN = "NzkxODk2MTE3MzA1OTMzODI1.X-V0uw.wEhmJtSnH53DQ0VyvWqXdJlqqkE"
		print("Bot is running..!")
		super().run(self.TOKEN,reconnect=True)

	async def process_commands(self, message):
		ctx = await self.get_context(message, cls=Context)

		if ctx.command is not None:
			if not self.ready:
				await ctx.send("I'm not ready to receive commands. Please wait a few seconds.")

			else:
				await self.invoke(ctx)

	async def on_connect(self):
		print("Bot is connected..!")

	async def on_disconnect(self):
		print("Bot is disconnected..!")

	async def on_error(self,err,*args,**kwargs):
		if err=="on_command_error":
			await args[0].send("Something went wrong!")
		
		# await args[0].send("Something went wrong!")
		raise 

	async def on_command_error(self,ctx,exc):
		if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
			pass

		elif isinstance(exc, MissingRequiredArgument):
			await ctx.send("One or more required arguments are missing.")

		elif isinstance(exc, CommandOnCooldown):
			retry_sec = self.pretty_print_time(ceil(exc.retry_after))
			await ctx.send(f"That command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Try again in {retry_sec}")

		elif hasattr(exc, "original"):

			if isinstance(exc.original, Forbidden):
				await ctx.send("I do not have permission to do that.")

			else:
				raise exc.original

		else:
			raise exc

	async def on_ready(self):
		if not self.ready:
			while not self.cogs_ready.all_ready():
				await sleep(0.5)
			self.ready = True
			await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="~help"))
			print("Bot is ready")
		else:
			print("Bot reconnected!")

	async def on_message(self,message):
		if not message.author.bot:
			await self.process_commands(message)

bot = Bot()