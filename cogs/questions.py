import discord
from discord.ext import commands
import datetime
import requests
import os
from dotenv import load_dotenv
load_dotenv()

class Questions(commands.Cog):
    url = os.getenv("API_URL");
    
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def daily(self, ctx):
        r = requests.get(f'{self.url}/daily');
        json_data = r.json();
        embed = discord.Embed(
            title=json_data['questionTitle'],
            url=f"https://leetcode.com/problems/{json_data['titleSlug']}/",
            description=json_data['question'],
            color=0xf89e1a
        )

        embed.add_field(name="Question ID", value=json_data['questionFrontendId'], inline=True)
        embed.add_field(name="Difficulty", value=json_data['difficulty'], inline=True)
        
        topic_tags = ", ".join([tag['name'] for tag in json_data['topicTags']])
        embed.add_field(name="Topic Tags", value=topic_tags, inline=False)

        testcases = json_data['exampleTestcases'].split('\n')
        for i, testcase in enumerate(testcases, 1):
            if testcase:
                embed.add_field(name=f"Example {i}", value=f"Input: {testcase}", inline=False)

        if 'constraints' in json_data:
            embed.add_field(name="Constraints", value=json_data['constraints'], inline=False)

        embed.set_footer(text=f"Date: {datetime.date.fromisoformat(json_data['date'])}")

        await ctx.send(embed=embed)
        
        

    @commands.command()
    async def problems(self, ctx, *args):
        # Parse arguments
        tags = []
        limit = None
        for arg in args:
            if arg.startswith('limit='):
                try:
                    limit = int(arg.split('=')[1])
                except ValueError:
                    await ctx.send("Invalid limit value. Please use a number.")
                    return
            else:
                tags.append(arg)

        # Construct URL
        base_url = f'{self.url}/problems'
        params = {}
        if tags:
            params['tags'] = '+'.join(tags)
        if limit:
            params['limit'] = str(limit)

        # Fetch problem data
        response = requests.get(base_url, params=params)
        data = response.json()

        # Create embed
        embed = discord.Embed(
            title="LeetCode Problems",
            description=f"Total Questions: {data['totalQuestions']} | Showing: {data['count']}",
            color=0xf89e1a
        )

        # Add problems to embed
        for problem in data['problemsetQuestionList']:
            problem_info = (
                f"Difficulty: {problem['difficulty']} | "
                f"Success Rate: {problem['acRate']:.2f}% | "
                f"Tags: {', '.join(tag['name'] for tag in problem['topicTags'])}"
            )
            embed.add_field(
                name=f"{problem['questionFrontendId']}. {problem['title']}",
                value=problem_info,
                inline=False
            )

        # Send embed
        await ctx.send(embed=embed)
    
async def setup(client):
    await client.add_cog(Questions(client));