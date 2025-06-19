import discord
from discord import Intents
from discord import Streaming
from discord.ext import commands
from discord.utils import get
import logging
import asyncio
from dotenv import load_dotenv
import random
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.all()

# Bot prefix.
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

# Server roles. Edit these to your exact roles.
role1 = "Member"
role2 = "Moderation"

# Server channels. Edit these to your exact channels.
channel1 = "「👋🏼」welcome"

# Console message when bot is ready.
@bot.event
async def on_ready():
    print (f"{bot.user.name} is ready to go!")
    return

# Member join event. Also assigns the Member role.
# Make sure the channel exists in your server,
# or change the variable `channel1` to the name of the channel you want to assign.
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=role1)
    if role:
        await member.add_roles(role)
    channel = discord.utils.get(member.guild.text_channels, name=channel1)
    if channel:
        await channel.send(
            f"Welcome {member.mention} to my Discord server! 🎉\n"
            f"If you came here to test out Onebot, use /help for a list of all commands.\n"
            f"For issues, chat in issues channel. Not available all the time."
        )

# Member leave event. Make sure the channel exists in your server,
# or change the variable `channel1` to the name of the channel you want to assign.
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name=channel1)
    if channel:
        await channel.send(f"Byebye! {member.mention}\n"
        "👋🏼"
        )
        return

# Test command.
@bot.command()
async def test(ctx):
    if ctx.guild is None:
        return
    else:
        await ctx.send("Test ✅")

# Hello command. Sends a greeting message to the user.
@bot.command()
async def hello(ctx):
    if ctx.guild is None:
        return
    else:
        await ctx.send(f"Hello {ctx.author.mention}!")

# Bye command. Sends a goodbye message to the user.
@bot.command()
async def bye(ctx):
    await ctx.send(f"Goodbye {ctx.author.mention}, see you next time!")

# Ping command. Sends the bot's latency in milliseconds.
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {ctx.author.mention} Your ping is {round(bot.latency * 1000)}ms.")

# Help command. Commands listed in commands.txt
@bot.command()
async def help(ctx):
    if ctx.guild is None:
        return
    embed = discord.Embed(title="OneBot Commands", description="List of available commands:")
    with open('commands.txt', 'r') as f:
        contents = f.read()
    embed.add_field(name="Commands", value=f"```{contents}```", inline=False)
    await ctx.send(embed=embed)

# Bot information command.
@bot.command()
async def info(ctx):
    if ctx.guild is None:
        return
    embed = discord.Embed(title="OneBot Info", description=(
        "This is a multi-purpose Discord bot.\n"
        "It can help with moderation, information, and more.\n"
        "Written in Python using the discord.py library.\n"
        "For more information, visit the [GitHub repository]"
        )
    )
    embed.set_thumbnail(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)

# Poll command.
@bot.command()
async def poll(ctx, *, question):
    if ctx.guild is None:
        return
    embed = discord.Embed(title="Poll (Yes/No)", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")
    await asyncio.sleep(3600)
    if asyncio.sleep(3600):
        await poll_message.clear_reactions()
        await ctx.send("Poll is closed. ⏰")

bot.run(token, log_handler=handler, log_level=logging.INFO)