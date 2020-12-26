from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown
from discord import Embed,File
from aiohttp import request
from typing import Optional
import datetime as dt
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
import os
from collections import namedtuple, deque

Rank = namedtuple('Rank', 'low high title title_abbr color_graph color_embed')

RATED_RANKS = (
    Rank(-10 ** 9, 1200, 'Newbie', 'N', '#CCCCCC', 0x808080),
    Rank(1200, 1400, 'Pupil', 'P', '#77FF77', 0x008000),
    Rank(1400, 1600, 'Specialist', 'S', '#77DDBB', 0x03a89e),
    Rank(1600, 1900, 'Expert', 'E', '#AAAAFF', 0x0000ff),
    Rank(1900, 2100, 'Candidate Master', 'CM', '#FF88FF', 0xaa00aa),
    Rank(2100, 2300, 'Master', 'M', '#FFCC88', 0xff8c00),
    Rank(2300, 2400, 'International Master', 'IM', '#FFBB55', 0xf57500),
    Rank(2400, 2600, 'Grandmaster', 'GM', '#FF7777', 0xff3030),
    Rank(2600, 3000, 'International Grandmaster', 'IGM', '#FF3333', 0xff0000),
    Rank(3000, 10 ** 9, 'Legendary Grandmaster', 'LGM', '#AA0000', 0xcc0000)
)

class Plot(Cog):
	def __init__(self,bot):
		self.bot = bot
		

	async def username_plot(self,username):
		url = f"https://codeforces.com/api/user.rating?handle={username}"
		
		async with request('GET',url,headers={}) as response:
			if response.status == 200:
				data = await response.json()
				data = data['result']
				rating = []
				time = []
				for submission  in data:
					rating.append(submission["newRating"])
					time.append(dt.datetime.fromtimestamp(submission["ratingUpdateTimeSeconds"]))
				return True,rating,time
			else:
				data = await response.json()
				data = data["comment"]
				return False,data,None
		


	@command(name="plotr",aliases=["pr"])
	@cooldown(1,60*5,BucketType.user)
	async def plot_rating(self,ctx,username:str,username_2: Optional[str] = None,username_3: Optional[str] = None):
		"""
		Rating graph of the username specified will be ploted. Also more than one user but at most of 3 users, rating graph can be plotted with the help of which one can easily compare.
		"""
		
		username_1_flag,rating_1,time_1 = await self.username_plot(username)
		if username_1_flag:
			plt.plot(time_1,rating_1,linestyle='-',marker='o',markersize=3,markeredgewidth=0.5,label=f"{username}")
			if username_2 is not None:
				username_2_flag,rating_2,time_2 = await self.username_plot(username_2)
				if username_2_flag:
					plt.plot(time_2,rating_2,linestyle='-',marker='o',markersize=3,markeredgewidth=0.5,label=f"{username_2}")
					if username_3 is not None:
						username_3_flag,rating_3,time_3 = await self.username_plot(username_3)
						if username_3_flag:
							plt.plot(time_3,rating_3,linestyle='-',marker='o',markersize=3,markeredgewidth=0.5,label=f"{username_3}")
						else:
							await ctx.send(f"Error occured!, **Comment** = {rating_3}")
							return
				else:
					await ctx.send(f"Error occured!, **Comment** = {rating_2}")
					return
		else:
			await ctx.send(f"Error occured!, **Comment** = {rating_1}")
			return
		
		"""
		Following are the tweaks done in the graph to make it look pretty
		"""
		ymin, ymax = plt.gca().get_ylim()
		bgcolor = plt.gca().get_facecolor()
		for rank in RATED_RANKS:
			plt.axhspan(rank.low, rank.high, facecolor=rank.color_graph, alpha=0.8, edgecolor=bgcolor, linewidth=0.5)

		locs, labels = plt.xticks()
		for loc in locs:
			plt.axvline(loc, color=bgcolor, linewidth=0.5)
		plt.ylim(ymin, ymax)
		plt.gcf().autofmt_xdate()
		plt.gca().fmt_xdata = mdates.DateFormatter('%Y:%m:%d')
		plt.title('Rating Graph')
		plt.legend()
		plt.savefig("rating_graph.png")

		await ctx.send(file=File("rating_graph.png"))
		os.remove("rating_graph.png")

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("plot")

	
def setup(bot):
	bot.add_cog(Plot(bot))
