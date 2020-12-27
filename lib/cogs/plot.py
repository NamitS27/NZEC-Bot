from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown
from discord import Embed,File
from aiohttp import request
from typing import Optional
import datetime as dt
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
import os
from collections import namedtuple

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

class ULegend:
	def __init__(self,s):
		self.string = s

	def __str__(self):
		return self.string

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

	async def generate_solved_problems_ratings(self,username):
		url=f"https://codeforces.com/api/user.status?handle={username}"
		async with request('GET',url) as response:
			if response.status == 200:
				data = await response.json()
				data = data["result"]
				rating = []
				for problem in data: 
					try:
						ratng = problem["problem"]["rating"]
					except:
						continue
					rating.append(ratng)
				return True,rating
			else:
				data = await response.json()
				data = data["comment"]
				return False,data
		


	@command(name="plotr",aliases=["pr"])
	@cooldown(1,30,BucketType.user)
	async def plot_rating(self,ctx,username:str,username_2: Optional[str] = None,username_3: Optional[str] = None):
		"""
		Rating graph of the username specified will be ploted. Also more than one user but at most of 3 users, rating graph can be plotted with the help of which one can easily compare.
		"""
		usernames = []
		username_1_flag,rating_1,time_1 = await self.username_plot(username)
		if username_1_flag:
			plt.plot(time_1,rating_1,linestyle='-',marker='o',markersize=3,markeredgewidth=0.5,markerfacecolor='white')
			usernames.append(f'{username} ({rating_1[len(rating_1)-1]})')
			if username_2 is not None:
				username_2_flag,rating_2,time_2 = await self.username_plot(username_2)
				if username_2_flag:
					plt.plot(time_2,rating_2,linestyle='-',marker='o',markersize=3,markeredgewidth=0.5,markerfacecolor='white')
					usernames.append(f'{username_2} ({rating_2[len(rating_2)-1]})')
					if username_3 is not None:
						username_3_flag,rating_3,time_3 = await self.username_plot(username_3)
						if username_3_flag:
							plt.plot(time_3,rating_3,linestyle='-',marker='o',markersize=3,markeredgewidth=0.5,markerfacecolor='white')
							usernames.append(f'{username_3} ({rating_3[len(rating_3)-1]})')
						else:
							await ctx.send(embed=Embed(description=f"Error occured!, **Comment** = {rating_3}"))
							return
				else:
					await ctx.send(embed=Embed(description=f"Error occured!, **Comment** = {rating_2}"))
					return
		else:
			await ctx.send(embed=Embed(description=f"Error occured!, **Comment** = {rating_1}"))
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
		plt.legend([ULegend(username) for username in usernames])
		plt.savefig("rating_graph.png")
		plt.gcf().clear()
		plt.close()

		await ctx.send(file=File("rating_graph.png"))
		os.remove("rating_graph.png")

	@command(name="plots",aliases=["ps"])
	async def plot_solved_graph(self,ctx,username: str,username_2: str,*,other_usernames:Optional[str] = None):
		usernames = [username,username_2]
		if other_usernames is not None:
			usernames += other_usernames.split(" ")
		hist_ratings = []
		labels = []
		for username in usernames:
			flag,rating = await self.generate_solved_problems_ratings(username)
			if flag:
				hist_ratings.append(rating)
				labels.append(f"{username}: {len(rating)}")
				continue
			else:
				await ctx.send(embed=Embed(title="Error!",description=rating))
				return
		
		plt.grid(color='grey',alpha=0.9,linestyle='-',linewidth=0.3)
		plt.hist(hist_ratings)
		plt.legend(labels)
		plt.xlabel("Rating")
		plt.ylabel("Number of Problems Solved")
		plt.title("Comparison!")
		plt.savefig("histograms_solved.png")
		plt.gcf().clear()
		plt.close()
		await ctx.send(file=File("histograms_solved.png"))
		os.remove("histograms_solved.png")

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("plot")

	
def setup(bot):
	bot.add_cog(Plot(bot))
