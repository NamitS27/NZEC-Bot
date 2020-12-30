from discord.ext.commands import Cog
from discord.ext.commands import command,BadArgument
from discord import Embed
from aiohttp import request
import random
from typing import Optional

class Contest(Cog):
	def __init__(self,bot):
		self.bot = bot

	def parse_args(self,args):
		usernames = []
		tags = ""
		args = args.split(' ')
		for argument in args:
			if argument[0] != '"':
				usernames.append(argument)
			else:
				tags += f'{argument[1:len(argument)-1]};'
		if len(tags)>1:
			if tags[len(tags)-1]==';':
				tags = tags[:len(tags)-1]
		
		return usernames,tags

	async def generate_solved_problems_names(self,username):
		url=f"https://codeforces.com/api/user.status?handle={username}"
		async with request('GET',url) as response:
			if response.status == 200:
				data = await response.json()
				data = data["result"]
				names = []
				for problem in data: 
					if problem["verdict"]=="OK":
						names.append(problem["problem"]["name"])
				return True,names
			else:
				data = await response.json()
				data = data["comment"]
				return False,data

	async def get_problems(self,tags):
		url=f"https://codeforces.com/api/problemset.problems?tags={tags}"
		async with request('GET',url) as response:
			if response.status == 200:
				data = await response.json()
				data = data["result"]["problems"]
				problems = []
				for problem in data:
					try:
						cid = problem["contestId"]
						rating = problem["rating"]
					except:
						continue
					problems.append((problem["name"],problem["index"],cid,rating))
				return True,problems
			else:
				data = await response.json()
				data = data["comment"]
				return False,data

	async def get_rating(self,usernames):
		username = ";".join(usernames)
		url = f"https://codeforces.com/api/user.info?handles={username}"
		async with request('GET',url) as response:
			if response.status == 200:
				ratings = []
				data = await response.json()
				data = data["result"]
				for info in data:
					ratings.append(info["rating"])
				return True,ratings
			else:
				data = await response.json()
				data = data["comment"]
				return False,data

	@command(name="mashup",aliases=["cmash"],usage="mashup|cmash <username> [tags]",brief="Creates a smart mashup of problems")
	async def create_mashup(self,ctx,*,args: str):
		"""
		Creates the mashup of 4 problems on the basis of the arguments which can be given as follows,
		usernames : the user can give space seperated codeforces handles of the people for whom they wish to create a mashup.
		tags : tags are to be given space seperated quoted using double quotes("tag") which are used to find the problems related to this tags.
		"""
		usernames,tags = self.parse_args(args)
		solved = []
		for username in usernames:
			flag,names= await self.generate_solved_problems_names(username)
			if not flag:
				ctx.send(embed=Embed(description=f"Error Occured!\n**Comment** : {names}"))
				return
			solved += names

		problem_flag,problems = await self.get_problems(tags)
		if not problem_flag:
			await ctx.send(embed=Embed(description=f"Error Occured!\n**Comment** : {problems}"))
			return 
		rating_flag,user_rating = await self.get_rating(usernames)
		
		if not rating_flag:
			await ctx.send(embed=Embed(description=f"Error Occured!\n**Comment** : {user_rating}"))
			return
		avg_rating = sum(user_rating)//len(usernames)
		
		possible_suggestions = []
		for name,index,cid,rating in problems:
			if name not in solved and rating-avg_rating <= 100 and rating-avg_rating >= -150:
				link = f"https://www.codeforces.com/problemset/problem/{cid}/{index}"
				possible_suggestions.append((index,name,link,rating))
		
		if len(possible_suggestions)<4:
			await ctx.send(embed=Embed(description="Cannot create mashup for the given handles!"))
			return
		
		mashup_problems = []
		while len(mashup_problems)!=4:
			index = random.randint(0,len(possible_suggestions)-1)
			if possible_suggestions[index] not in mashup_problems:
				mashup_problems.append(possible_suggestions[index])
		
		description = ""
		indexes = ['A','B','C','D']
		i = 0
		for ind,name,link,rating in mashup_problems:
			description += f"[{indexes[i]}. {name}]({link}) [{rating}]\n\n"
			i += 1

		message = "Mashup for"
		for user in usernames:
			message += f' `{user}`,'
		message = message[:len(message)-1]
		embed = Embed(description=description,colour=0xF22324)		 
		await ctx.send(message,embed=embed)
		

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("contest")

	
def setup(bot):
	bot.add_cog(Contest(bot))
