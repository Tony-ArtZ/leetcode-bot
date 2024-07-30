import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="LeetCode Bot Help", description="Here are the available commands:", color=0xf89e1a)

        embed.add_field(name="User Commands", value="""
        `!store (leetcode username)`: Store your LeetCode username
        `!profile (me/leetcode username)`: View LeetCode profile
        `!badges (me/leetcode username)`: View LeetCode badges
        `!submissions (me/leetcode username)`: View recent submissions
        `!solved (me/leetcode username)`: View solved problems
        """, inline=False)

        embed.add_field(name="Question Commands", value="""
        `!daily`: Get the daily LeetCode challenge
        `!problems (limit=num and other tags)`: Search for LeetCode problems
        """, inline=False)

        embed.set_footer(text="Use 'me' as an argument to refer to your stored username.")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))