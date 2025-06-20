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
channel2 = "「👨🏼‍💻」github-updates"

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

# Ensures bot is private.
@bot.event
async def on_guild_join(guild):
    allowed_guild_ids = [ID_HERE]  # Replace with your server ID
    if guild.id not in allowed_guild_ids:
        await guild.leave()

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
        "For more information, visit the [GitHub repository](https://github.com/Maurice-95/onebot-discord)"
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

# Member count command.
@bot.command()
async def membercount(ctx):
    if ctx.guild is None:
        return
    embed = discord.Embed(title="Member Count", description=f"Total members in this server: {ctx.guild.member_count} 👥")
    embed.set_thumbnail(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)

# User info command.
@bot.command()
async def userinfo(ctx):
    if ctx.guild is None:
        return
    embed = discord.Embed(title="User Info", description=f"Information about {ctx.author.mention}")
    embed.add_field(name="Username", value=ctx.author.name, inline=True)
    embed.add_field(name="ID", value=ctx.author.id, inline=True)
    embed.add_field(name="Created At", value=ctx.author.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name="Joined At", value=ctx.author.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.set_thumbnail(url=ctx.author.avatar.url)
    await ctx.send(embed=embed)

# "Fun" commands.

# Dice roll command.
@bot.command()
async def dice(ctx, sides: int=6):
    if ctx.guild is None:
        return
    a = random.randint(1, 6)
    await ctx.send(f"{ctx.author.mention} rolled and got {a}! 🎲")

# Coin flip command.
@bot.command()
async def coinflip(ctx):
    if ctx.guild is None:
        return
    a = random.choice(["Heads", "Tails"])
    await ctx.send(f"{ctx.author.mention} flipped a coin and got {a}! 🪙")

# Rock, Paper, Scissors command.
@bot.command()
async def rps(ctx, choice: str):
    if ctx.guild is None:
        return
    choices = ["rock", "paper", "scissors"]
    user_choice = choice.lower()
    if user_choice not in choices:
        await ctx.send(f"{ctx.author.mention} Please choose rock, paper, or scissors.")
        return

    bot_choice = random.choice(choices)
    if choice.lower() == bot_choice:
        await ctx.send(f"It's a tie! We both chose {bot_choice}.")
    elif (user_choice == "rock" and bot_choice == "scissors") or \
         (user_choice == "paper" and bot_choice == "rock") or \
         (user_choice == "scissors" and bot_choice == "paper"):
        await ctx.send(f"{ctx.author.mention} You win! I chose {bot_choice}.")
    else:
        await ctx.send(f"{ctx.author.mention} You lose! I chose {bot_choice}.")

@rps.error
async def rps_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} Please choose rock, paper, or scissors.")

#Quote command.
@bot.command()
async def quote(ctx):
    if ctx.guild is None:
        return
    with open('quotes.txt', 'r') as f:
        quotes = f.readlines()
    quote = random.choice(quotes).strip()
    await ctx.send(f"{quote}")

#Administration commands.

# Announcement command.
@bot.command()
async def announce(ctx, *, message):
    if ctx.guild is None:
        return
    channel = discord.utils.get(ctx.guild.text_channels, name=channel2)
    if any(role.name in role2 for role in ctx.author.roles):
        if channel:
            await channel.send(f"💥Announcement💥: {message}")
        else:
            await ctx.send("Announcement channel not found.")
    else:
        await ctx.send("You don't have permission to do that!")

# Clear chat command. Clears chat when using a value of /clear 1 or greater.
@bot.command()
async def clear(ctx, amount: int):
    if ctx.guild is None:
        return
    if any(role.name in role2 for role in ctx.author.roles):
        if amount < 1:
            await ctx.send("You must delete at least one message.")
            return
        deleted = await ctx.channel.purge(limit=amount + 1)
    else:
        await ctx.send(f"You don't have permission to do that!")

# Slow mode command.
@bot.command()
async def slowmode(ctx, seconds: int):
    if not ctx.channel.permissions_for(ctx.guild.me).manage_channels:
        await ctx.send("⛔ I don’t have permission to manage this channel!")
        return
    if seconds < 0:
        await ctx.send("⛔ Slowmode duration must be zero or more seconds.")
        return
    if seconds > 21600:  # Discord max slowmode is 6 hours
        await ctx.send("⛔ Slowmode duration cannot exceed 21600 seconds (6 hours).")
        return
    role = discord.utils.get(ctx.guild.roles, name=role2)
    await ctx.channel.edit(slowmode_delay=seconds)
    if seconds == 0:
        await ctx.send("✅ Slowmode has been disabled in this channel.")
    else:
        await ctx.send(f"✅ Slowmode set to {seconds} seconds in this channel.")
        if any(role.name in role2 for role in ctx.author.roles) is None:
            await ctx.send("You don't have permission to do that!")

# Warn command.
@bot.command()
async def warn(ctx, *, reason=None):
    if ctx.guild is None:
        return
    if any(role.name in role2 for role in ctx.author.roles):
        if ctx.message.mentions:
            for member in ctx.message.mentions:
                with open('warnings.txt', 'a') as f:
                    f.write(f"Warned at {ctx.message.created_at}. Mod: {ctx.author.name} Reason: {reason}\n")
                await ctx.send(f"{member.mention} has been warned! ⚠️ Please remember to follow the rules. Reason: {reason}")
        else:
            await ctx.send("You need to mention a user to warn them.")
    else:
        await ctx.send(f"You don't have permission to do that!")

# Warn list command.
@bot.command()
async def warnlist(ctx):
    if ctx.guild is None:
        return
    with open('warnings.txt', 'r') as f:
        warnings = f.readlines()
    if any(role.name in role2 for role in ctx.author.roles):
        if warnings:
            embed = discord.Embed(title="Warning List", description="List of warnings:")
            for warning in warnings:
                embed.add_field(name="Warning", value=warning.strip(), inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("No warnings found.")
    else:
        await ctx.send(f"You don't have permission to do that!")
    
bot.run(token, log_handler=handler, log_level=logging.INFO)