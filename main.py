import discord
from discord.ext import commands, tasks
import os
import requests
import asyncio
from dotenv import load_dotenv
load_dotenv()

client = commands.Bot(command_prefix = '!', intents=discord.Intents.all());
client.remove_command('help');

@client.event
async def on_ready():
    print('Bot is ready')
    changeStatus.start()
    
    
@tasks.loop(hours=24)
async def changeStatus():
    r = requests.get(f'https://alfa-leetcode-api.onrender.com/daily');
    json_data = r.json();
        
    question_title = json_data['questionTitle']
    difficulty = json_data['difficulty']
    question_link = json_data['questionLink']
        
    status = f"⭐ {question_title} ({difficulty}) | {question_link}"
    await client.change_presence(activity=discord.Game(name=status))


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename[:-3]}');
            
            
            
async def main():
    await load();
    await client.start(os.getenv("DISCORD_TOKEN"));
    
asyncio.run(main());