from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown
from discord import Embed
from prettytable import PrettyTable
from aiohttp import request

class UserServer(Cog):
    def __init__(self,bot):
        self.bot = bot

    async def check_username(self,handle):
        url=f"https://codeforces.com/api/user.info?handles={handle}"
        async with request('GET',url) as response:
            if response.status == 200:
                return True
            else:
                return False


    @command(name="setu",brief="Setting the cf username with own discord user")
    async def set_user(self,ctx,username):
        """
        Sets the codeforces username provided by the user along with the user setting it for that server.
        """
        username_test = await self.check_username(username)
        if not username_test:
            await ctx.send(embed=Embed(title="Invalid CodeForces username!"))
            return 

        user_id = str(ctx.author.id)
        server_id = str(ctx.message.guild.id)
        data = self.bot.db.fetch_all('server_det')
        flag=False
        for pid,sid,uid,cfu,time in data:
            if sid==server_id and user_id==uid:
                flag= True
                break
        if not flag:
            self.bot.db.insert_server_det(server_id,user_id,username)
            await ctx.send(embed=Embed(description=f"CodeForces username has been set to `{username}` for {ctx.author.mention}",colour=0x0037fa))
        else:
            await ctx.send(embed=Embed(description=f"You have already set your CodeForces username\nYou can update it using command `~updateu <new_username>`",colour=0x0037fa))

    @command(name="updateu",brief="Updating the set cf username with own discord user")
    async def update_user(self,ctx,username):
        """
        Updates the cf username which was set by the user with their own self.
        """
        username_test = await self.check_username(username)
        if not username_test:
            await ctx.send(embed=Embed(title="Invalid CodeForces username!"))
            return 

        user_id = str(ctx.author.id)
        server_id = str(ctx.message.guild.id)
        data = self.bot.db.fetch_all('server_det')
        flag=False
        for pid,sid,uid,cfu,time in data:
            if sid==server_id and user_id==uid:
                flag= True
                break
        if flag:
            self.bot.db.update_username(server_id,user_id,username)
            await ctx.send(embed=Embed(description=f"CodeForces username has been updated to `{username}` for {ctx.author.mention}",colour=0x0037fa))
        else:
            await ctx.send(embed=Embed(description=f"You haven't set your CodeForces username\nYou can set it using command `~setu <cf_username>`",colour=0x0037fa))

    async def get_user_rating(self,username):
        username = ";".join(username)
        url = f"https://codeforces.com/api/user.info?handles={username}"
        async with request('GET',url) as response:
            if response.status == 200:
                rr = []
                data = await response.json()
                data = data["result"]
                for info in data:
                    rr.append((info["rating"],info["rank"].upper()))
                return True,rr
            else:
                data = await response.json()
                data = data["comment"]
                return False,data

    @command(name="list",brief="Listing of server's user list who has set their cf handle")
    @cooldown(1,60,BucketType.guild)
    async def list_users(self,ctx):
        """
        Displays the list of the details of the user who has set their cf username along with their own selves
        """
        data =  self.bot.db.get_server_users(str(ctx.message.guild.id))
        if len(data)==0:
            await ctx.send(embed=Embed(title="There are no cf usernames set to display!"))
            return
        table = PrettyTable()
        table.field_names = ["User","CodeForces Handle","Rating","Rank"]
        usernames = []
        for pid,sid,uid,cfu,time in data:
            usernames.append(cfu)
        flag,rar = await self.get_user_rating(usernames)
        if not flag:
            await ctx.send(f"ERROR!\n**Comment** :  {rar}")
            return
        cnt = 0
        for pid,sid,uid,cfu,time in data:
            uname = await self.bot.fetch_user(f"{uid}")
            table.add_row([f"{uname.name}",cfu,rar[cnt][0],rar[cnt][1]])
            cnt += 1
        await ctx.send(f"```swift\n{table}\n```")


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("user_server")


def setup(bot):
	bot.add_cog(UserServer(bot))
