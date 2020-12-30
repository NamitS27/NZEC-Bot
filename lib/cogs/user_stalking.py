from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown
from discord import Embed
from aiohttp import request

class UserStalking(Cog):
	def __init__(self,bot):
		self.bot = bot

	def rating_to_color(self,rating):
		"""
		returns hex value corresponding to rating
		"""
		colors = [0xCCCCCC,0x77FF77,0x77DDBB,0xAAAAFF,0xFF88FF,0xFFCC88,0xFFBB55,0xFF7777,0xFF3333,0xAA0000]

		if rating == "Unrated" or rating<1200:
			return colors[0]
		elif rating >= 1200 and rating < 1400:
			return colors[1]
		elif rating >=1400 and rating < 1600:
			return colors[2]
		elif rating >=1600 and rating < 1900:
			return colors[3]
		elif rating >= 1900 and rating < 2100:
			return colors[4]
		elif rating >=2100 and rating < 2300:
			return colors[5]
		elif rating >=2400 and rating < 2400:
			return colors[6]
		elif rating >=2400 and rating < 2600:
			return colors[7]
		elif rating >=2600 and rating < 2300:
			return colors[8]
		else:
			return colors[9]


	@command(name="stalk",aliases=["stk"],brief='Gives at most 5 latest submission done by the username provided')
	@cooldown(1,60,BucketType.user)
	async def stalk(self,ctx,username: str):
		"""
		By the help of this command one can see the recent submissions made by the codeforces username specified and hence can stalk him :)
		"""
		url = f"https://codeforces.com/api/user.status?handle={username}&from=1&count=5"
		async with request('GET',url,headers={}) as response:
			if response.status == 200:
				
				data = await response.json()
				data = data['result']
				desc = ""
				for submission  in data:
					index = submission["problem"]["index"]
					contest_id = submission["problem"]["contestId"]
					problem_name = submission["problem"]["name"]
					flag=0
					try:
						rating = submission["problem"]["rating"]
					except:
						try:
							flag = 1
							points = submission["problem"]["points"]
						except:
							flag = 2
					link = f'https://www.codeforces.com/problemset/problem/{contest_id}/{index}'
					if flag==0:
						desc += f'[{index}. {problem_name}]({link}) [{rating}]\n\n'
					elif flag==1:
						desc += f'[{index}. {problem_name}]({link}) [{int(points)}]\n\n'
					else:
						desc += f'[{index}. {problem_name}]({link})\n\n'
				
				stalk_embed = Embed(title=f"Recent Submissions of user {username}",description=desc)
				await ctx.send(embed=stalk_embed)
			else:
				data = await response.json()
				data = data["comment"]
				await ctx.send(f"Error! : *{data}*")

	@command(name="profile",aliases=["prof"],brief='Displays the profile of the provided username')
	# @cooldown(1,15,BucketType.user)
	async def get_profile(self,ctx,username: str):
		"""
		This command is helpful for viewing the basic profile of the codeforces username specified.
		"""
		url = f"https://codeforces.com/api/user.info?handles={username}"
		async with request('GET',url,headers={}) as response:
			if response.status == 200:
				stalk_embed = Embed(title=f"Profile of *{username}* !")
				data = await response.json()
				data = data['result'][0]
				try:
					rating = data["rating"]
				except:
					rating = "Unrated"
				rank = data["rank"]
				max_rating = data["maxRating"]
				avatar_url = "https:"+data["avatar"]
				stalk_embed.colour = self.rating_to_color(rating)
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
