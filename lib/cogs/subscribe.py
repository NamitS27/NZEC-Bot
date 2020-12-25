from discord.ext.commands import Cog
from discord.ext.commands import command,BadArgument

class Subscribe(Cog):
	def __init__(self,bot):
		self.bot = bot

	@command(name="subscribe",aliases=["sub","s"],brief='Subscribes the user who enters the command')
	async def subscribe(self,ctx):
		await ctx.send(f"{ctx.author.mention}, You have been successfully subscribed!")

	@subscribe.error
	async def subscribe_error(self,ctx,exc):
		if isinstance(exc,BadArgument):
			await ctx.send("Bad Argument Error!")

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("subscribe")

	
def setup(bot):
	bot.add_cog(Subscribe(bot))
