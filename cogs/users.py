from discord.ext import commands
import requests
import sys
import discord
import os
import datetime
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.jsonUtil import store, get;

class Users(commands.Cog):
    url = os.getenv("API_URL");
    
    def __init__(self, client):
        self.client = client        
        
    # Store user information
    @commands.command()
    async def store(self, ctx, leetcodeId):
        store(ctx.author.id, leetcodeId);
        await ctx.send(f'Stored! <@{ctx.author.id}>');
    
    
    # Get user information
    @commands.command()
    async def profile(self, ctx, userId):
        if(userId == "me"):
            userId = get(str(ctx.author.id));
            if userId is None:
                await ctx.send("Please store your LeetCode username first using `!store (leetcode username)`");
                return;
                        
        r = requests.get(f'{self.url}/{userId}');
        json_data = r.json();
        
        embed = discord.Embed(title=f"{json_data['name']}'s Profile", color=0xf89e1a)
        
        # Set the thumbnail to the user's avatar
        embed.set_thumbnail(url=json_data['avatar'])
        
        # Add fields to the embed
        embed.add_field(name="Username", value=json_data['username'], inline=True)
        embed.add_field(name="Birthday", value=json_data['birthday'], inline=True)
        embed.add_field(name="Country", value=json_data['country'], inline=True)
        embed.add_field(name="Ranking", value=json_data['ranking'], inline=True)
        embed.add_field(name="Reputation", value=json_data['reputation'], inline=True)
        
        # Add skill tags
        skills = ", ".join(json_data['skillTags'])
        embed.add_field(name="Skills", value=skills, inline=False)
        
        # Add social links
        social_links = []
        if json_data['gitHub']:
            social_links.append(f"[GitHub]({json_data['gitHub']})")
        if json_data['linkedIN']:
            social_links.append(f"[LinkedIn]({json_data['linkedIN']})")
        if json_data['twitter']:
            social_links.append(f"[Twitter]({json_data['twitter']})")
        if json_data['website']:
            social_links.append(f"[Website]({json_data['website'][0]})")
        
        embed.add_field(name="Social Links", value=" | ".join(social_links), inline=False)
        
        # Set the footer
        embed.set_footer(text="User Information")
        
        # Send the embed
        await ctx.send(embed=embed)
        
        
    # Get user badge information
    @commands.command()
    async def badges(self, ctx, userId):
        if(userId == "me"):
            userId = get(str(ctx.author.id));
            if userId is None:
                await ctx.send("Please store your LeetCode username first using `!store (leetcode username)`");
                return;
        
        r = requests.get(f'{self.url}/{userId}/badges');
        json_data = r.json();
        
        embed = discord.Embed(title="User Badge Information", color=0xf89e1a)
        
        # Add badge count
        embed.add_field(name="Total Badges", value=json_data['badgesCount'], inline=False)
        
        # Add current badges
        if json_data['badges']:
            badge_names = ", ".join([badge['name'] for badge in json_data['badges']])
            embed.add_field(name="Current Badges", value=badge_names, inline=False)
        else:
            embed.add_field(name="Current Badges", value="No badges earned yet", inline=False)
        
        # Add upcoming badges
        if json_data['upcomingBadges']:
            upcoming_badges = "\n".join([badge['name'] for badge in json_data['upcomingBadges']])
            embed.add_field(name="Upcoming Badges", value=upcoming_badges, inline=False)
        else:
            embed.add_field(name="Upcoming Badges", value="No upcoming badges", inline=False)
        
        # Add active badge
        if json_data['activeBadge']:
            embed.add_field(name="Active Badge", value=json_data['activeBadge']['name'], inline=False)
            embed.set_thumbnail(url=json_data['activeBadge']['icon'])
        else:
            embed.add_field(name="Active Badge", value="No active badge", inline=False)
        
        # If there's an upcoming badge, use its icon as the thumbnail if no active badge
        if not json_data['activeBadge'] and json_data['upcomingBadges']:
            embed.set_thumbnail(url=f"https://leetcode.com{json_data['upcomingBadges'][0]['icon']}")
        
        # Set the footer
        embed.set_footer(text="Badge Information")
        
        # Send the embed
        await ctx.send(embed=embed)
        
        
    # Get user submission information
    @commands.command()
    async def submissions(self, ctx, userId):
        if(userId == "me"):
            userId = get(str(ctx.author.id));
            if userId is None:
                await ctx.send("Please store your LeetCode username first using `!store (leetcode username)`");
                return;
        
        r = requests.get(f'{self.url}/{userId}/submission');
        json_data = r.json();
                
        embed = discord.Embed(title="LeetCode Submissions", color=0xf89e1a)

        # Add total count of submissions
        embed.add_field(name="Total Submissions", value=json_data['count'], inline=False)

        # Add the most recent 5 submissions
        embed.add_field(name="Recent Submissions", value="", inline=False)

        for i, submission in enumerate(json_data['submission'][:5], 1):
            title = submission['title']
            status = submission['statusDisplay']
            timestamp = int(submission['timestamp'])
            
            embed.add_field(
                name=f"{i}. {title}",
                value=f"Status: {status}\nTimestamp: {datetime.datetime.fromtimestamp(timestamp)}",
                inline=False
            )

        # Add a footer
        embed.set_footer(text="LeetCode Submission Summary")

        # Send the embed
        await ctx.send(embed=embed)
        
        
    @commands.command()
    async def solved(self, ctx, userId):
        if(userId == "me"):
            userId = get(str(ctx.author.id));
            if userId is None:
                await ctx.send("Please store your LeetCode username first using `!store (leetcode username)`");
                return;
        
        r = requests.get(f'{self.url}/{userId}/solved');
        json_data = r.json();
        
        embed = discord.Embed(title="LeetCode Stats", color=0xf89e1a)
        
        # Add fields for solved problems
        embed.add_field(name="Total Solved", value=json_data["solvedProblem"], inline=True)
        embed.add_field(name="Easy Solved", value=json_data["easySolved"], inline=True)
        embed.add_field(name="Medium Solved", value=json_data["mediumSolved"], inline=True)
        embed.add_field(name="Hard Solved", value=json_data["hardSolved"], inline=True)

        # Add fields for submissions
        total_submissions = sum(item["submissions"] for item in json_data["totalSubmissionNum"])
        accepted_submissions = sum(item["submissions"] for item in json_data["acSubmissionNum"])
        
        embed.add_field(name="Total Submissions", value=total_submissions, inline=False)
        embed.add_field(name="Accepted Submissions", value=accepted_submissions, inline=True)
        
        # Calculate and add acceptance rate
        acceptance_rate = (accepted_submissions / total_submissions) * 100 if total_submissions > 0 else 0
        embed.add_field(name="Acceptance Rate", value=f"{acceptance_rate:.2f}%", inline=True)
        
        await ctx.send(embed=embed)
    
        
    
async def setup(client):
    await client.add_cog(Users(client))