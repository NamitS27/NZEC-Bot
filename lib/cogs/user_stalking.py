from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown
from discord import Embed
from aiohttp import request

class UserStalking(Cog):
	def __init__(self,bot):
		self.bot = bot

	@command(name="stalk",aliases=["stk"],brief='Gives at most 5 latest submission done by the username provided')
	@cooldown(1,60*5,BucketType.user)
	async def stalk(self,ctx,username: str):
		
		url = f"https://codeforces.com/api/user.status?handle={username}&from=1&count=5"
		async with request('GET',url,headers={}) as response:
			if response.status == 200:
				stalk_embed = Embed(title=f"Recent Submissions of user {username}")
				data = await response.json()
				data = data['result']
				for submission  in data:
					index = submission["problem"]["index"]
					problem_name = submission["problem"]["name"]
					rating = submission["problem"]["rating"]
					verdict = submission["verdict"]
					stalk_embed.add_field(name=f"[{index}] {problem_name}",value=f"Rating : {rating} | Verdict : {verdict}",inline=False)
				await ctx.send(embed=stalk_embed)
			else:
				data = await response.json()
				data = data["comment"]
				await ctx.send(f"Error! : *{data}*")

	@command(name="profile",aliases=["prof"],brief='Displays the profile of the provided username')
	@cooldown(1,15,BucketType.user)
	async def get_profile(self,ctx,username: str):
		url = f"https://codeforces.com/api/user.info?handles={username}"
		async with request('GET',url,headers={}) as response:
			if response.status == 200:
				stalk_embed = Embed(title=f"Profile of *{username}* !")
				data = await response.json()
				data = data['result'][0]
				rating = data["rating"]
				rank = data["rank"]
				max_rating = data["maxRating"]
				avatar_url = "https:"+data["avatar"]
				stalk_embed.add_field(name="Rating    ",value=f"{rating}",inline=False)
				stalk_embed.add_field(name="Max Rating    ",value=f"{max_rating}",inline=False)
				stalk_embed.add_field(name="Rank",value=f"{rank.upper()}",inline=False)
				stalk_embed.set_thumbnail(url=avatar_url)
				await ctx.send(embed=stalk_embed)
			else:
				data = await response.json()
				data = data["comment"]
				await ctx.send(f"Error! : *{data}*")


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("user_stalking")

	
def setup(bot):
	bot.add_cog(UserStalking(bot))
