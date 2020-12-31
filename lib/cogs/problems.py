from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown
from discord import Embed
from aiohttp import request
from typing import Optional
import random

class Problems(Cog):
	def __init__(self,bot):
		self.bot = bot

	async def get_contest_ids(self):
		url="https://codeforces.com/api/contest.list"
		async with request('GET',url) as response:
			if response.status == 200:
				data = await response.json()
				data = data["result"]
				ids = []
				for contest in data: 
					ids.append(contest["id"])
				return True,ids
			else:
				data = await response.json()
				data = data["comment"]
				return False,data

	async def generate_solved_problems_ids(self,username):
		url=f"https://codeforces.com/api/user.status?handle={username}"
		async with request('GET',url) as response:
			if response.status == 200:
				data = await response.json()
				data = data["result"]
				ids = []
				for problem in data: 
					if problem["verdict"]=="OK":
						ids.append(problem["contestId"])
				return True,ids
			else:
				data = await response.json()
				data = data["comment"]
				return False,data

	def create_problem_embed(self,problems):
		description = ""
		for index,name,link,rating,tags in problems:
			tags = ",".join(tags)
			description += f'[{index}. {name}]({link}) [{rating}]\nTags : *{tags}*\n\n'
		embed = Embed(description=description,colour=0xffffff)
		return embed


	@command(name="getproblems",aliases=["getp"],brief="Problem Suggestion on basis of arguments")
	@cooldown(1,60*2,BucketType.user)
	async def fetch_problems(self,ctx,username:str,min_rating:int,max_rating:int,*,tags: Optional[str] = ""):
		"""
		Gives the list of the problems on the basis of the codeforces username and the problems will be in the range of [minimum rating,maximum rating] as specified by the user. Also the user can specify the tags using "tag_name" (between double quotes)
		"""
		tags = ";".join([tag[1:len(tag)-1] for tag in tags.split(' ')])
		contest_flag,contests = await self.get_contest_ids()
		solved_flag,solved = await self.generate_solved_problems_ids(username)
		
		if contest_flag and solved_flag:
			url=f"https://codeforces.com/api/problemset.problems?tags={tags}"
			async with request('GET',url) as response:
				if response.status == 200:
					data = await response.json()
					data = data["result"]["problems"]
					ids = set(contests) - set(solved)
					problems = []
					give_problem = []
					cnt = 0
					for problem in data:
						if "*special" in problem['tags']:
							continue
						try:
							rating = problem['rating']
						except:
							rating = None
						if rating is not None:
							if problem["contestId"] in ids and (int(rating)>=min_rating and int(rating)<=max_rating):
								contest_id = problem["contestId"]
								problem_index = problem["index"]
								link = f"https://www.codeforces.com/problemset/problem/{contest_id}/{problem_index}"
								problems.append((problem_index,problem["name"],link,rating,problem["tags"]))
					index_list = random.sample(range(0,len(problems)-1), 5)
					for i in index_list:
						give_problem.append(problems[i])
					
					embed = self.create_problem_embed(give_problem)
					await ctx.send(f'Here are the problems for practice for `{username}`',embed=embed)					
				else:
					data = await response.json()
					data = data["comment"]
					await ctx.send(f"Error : {data}")
		else:
			await ctx.send("Some Error Occured!")

    
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("problems")

    

def setup(bot):
	bot.add_cog(Problems(bot))
