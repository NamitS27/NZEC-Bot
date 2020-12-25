from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown
from discord import Embed,File
from aiohttp import request
from typing import Optional
import datetime as dt
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
import os

class Plot(Cog):
	def __init__(self,bot):
		self.bot = bot

	def create_plot(self,x_axis,y_axis):
		plt.style.use('seaborn')
		plt.rcParams["figure.figsize"] = (12,7)
		fig,ax = plt.subplots(1)
		# fig.patch.set_facecolor('#F6F6F6')
		# fig.patch.set_alpha(0.9)
		plt.plot(x_axis,y_axis,linestyle='-',marker='o',markersize=3,markeredgewidth=0.5)
		fig.autofmt_xdate()
		ax.fmt_xdata = mdates.DateFormatter('%Y:%m:%d')
		plt.title('Rating Graph')
		plt.savefig("rating_graph.png")


	@command(name="plotr",aliases=["pr"])
	@cooldown(1,60*5,BucketType.user)
	async def plot_rating(self,ctx,username:str,username_2: Optional[str] = None,username_3: Optional[str] = None):
		"""
		Rating graph of the username specified will be ploted. Also more than one user but at most of 3 users, rating graph can be plotted with the help of which one can easily compare
		#TODO: adding plot of username_2 and username_3
		"""
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
				
				self.create_plot(time,rating)
				await ctx.send(file=File("rating_graph.png"))
				os.remove("rating_graph.png")
			else:
				data = await response.json()
				data = data["comment"]
				await ctx.send(f"Error! : *{data}*")

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("plot")

	
def setup(bot):
	bot.add_cog(Plot(bot))
