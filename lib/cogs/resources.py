from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown
from discord import Embed
from prettytable import PrettyTable
from aiohttp import request

class Resources(Cog):
    def __init__(self,bot):
        self.bot = bot

    @command(name="addr")
    async def add_resources(self,ctx,resource_link,tag):
        """
        #TODO: Breif and description is left
        """
        user_id = str(ctx.author.id)
        server_id = str(ctx.message.guild.id)
        try:
            self.bot.db.add_resource(server_id,user_id,tag,resource_link)
            await ctx.send("Resource submitted successfully!")
        except:
            await ctx.send("Some Error Occurred! Cannot add the resource")

    @command(name="findr")
    async def find_resources(self,ctx,tag):
        pass
        

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("resources")


def setup(bot):
	bot.add_cog(Resources(bot))
