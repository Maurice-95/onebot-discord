import discord
from discord import Intents
from discord import Streaming
from discord import Spotify
from discord.ext import commands
from discord.utils import get
import logging
import asyncio
import pytz
from datetime import datetime
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
channel3 = "bot-log"
channel4 = "「💭」suggestions"

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
        return

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
        return

# Test command.
@bot.command()
async def test(ctx):
    if ctx.guild is None:
        return
    else:
        await ctx.send("Test ✅")
        return

# Hello command. Sends a greeting message to the user.
@bot.command()
async def hello(ctx):
    if ctx.guild is None:
        return
    else:
        await ctx.send(f"Hello {ctx.author.mention}!")
        return

# Bye command. Sends a goodbye message to the user.
@bot.command()
async def bye(ctx):
    await ctx.send(f"Goodbye {ctx.author.mention}, see you next time!")
    return

# Ping command. Sends the bot's latency in milliseconds.
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {ctx.author.mention} Your ping is {round(bot.latency * 1000)}ms.")
    return

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
    return

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
    return

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
        return

@poll.error
async def poll_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please provide a question for the poll.")
        return

# Member count command.
@bot.command()
async def membercount(ctx):
    if ctx.guild is None:
        return
    embed = discord.Embed(title="Member Count", description=f"Total members in this server: {ctx.guild.member_count} 👥")
    embed.set_thumbnail(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)
    return

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
    return

# Shows user avatar.
@bot.command()
async def avatar (ctx):
    if ctx.guild is None:
        return
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
        embed = discord.Embed(title=f"{user.name}'s Avatar")
        embed.set_image(url=user.avatar.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("You need to mention a user to see their avatar.")
        return

# Roles command. Shows roles in an embed without @everyone.
@bot.command()
async def roles(ctx):
    if ctx.guild is None:
        return
    guild = ctx.guild
    roles = guild.roles
    role_mentions = [role.mention for role in roles if role != guild.default_role]
    embed = discord.Embed(title="Server Roles", description="")
    embed.add_field(name="Roles", value=", ".join(role_mentions), inline=False)
    await ctx.send(embed=embed)
    return

# Suggestion command. Sends a suggestion to the suggestions channel with polling.
@bot.command()
async def suggest(ctx, *, question):
    if ctx.guild is None:
        return
    channel = discord.utils.get(ctx.guild.text_channels, name=channel4)
    if channel:
        embed = discord.Embed(title="Onebot Suggestion", description=question)
        suggest_message = await channel.send(embed=embed)
        await suggest_message.add_reaction("👍")
        await suggest_message.add_reaction("👎")
        await ctx.send(f"Your suggestion has been sent to {channel.mention}. Thank you! 💡")
        return

@suggest.error
async def suggest_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} Please provide a suggestion.")
        return    

# Spotify playing command. Shows what the user is currently listening to on Spotify.
@bot.command()
async def spotify(ctx, member: discord.Member = None):
    if ctx.guild is None:
        return
    user = member or ctx.author
    activity = ctx.author.activity
    for activity in user.activities:
        if isinstance(activity, discord.Spotify):
            embed = discord.Embed(title=f"{ctx.author.name}'s Spotify", description=(
                f"**Song:** {activity.title}\n"
                f"**Artist:** {activity.artists}\n"
                )
            )
            embed.set_thumbnail(url=activity.album_cover_url)
            await ctx.send(embed=embed)
            return
    if user == ctx.author:
        await ctx.send("Seems like you're not listening to Spotify right now. 🎧")
        return
    else:
        await ctx.send(f"{user.mention} is not listening to Spotify right now. 🎧")
        return

# Sends invite link in chat.
@bot.command()
async def invite(ctx):
    if ctx.guild is None:
        return
    invite_link = "https://discord.gg/nrnGKy5JZh" # Replace with your bot's invite link
    embed = discord.Embed(title="Server invite", description=(
        "Copy the link below to invite users to this server.\n"
        f"[Click/copy this]({invite_link})."
        )
    )
    embed.set_thumbnail(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)
    return

# "Fun" commands.

# Dice roll command.
@bot.command()
async def dice(ctx, sides: int=6):
    if ctx.guild is None:
        return
    a = random.randint(1, 6)
    await ctx.send(f"{ctx.author.mention} rolled and got {a}! 🎲")
    return

# Coin flip command.
@bot.command()
async def coinflip(ctx):
    if ctx.guild is None:
        return
    a = random.choice(["Heads", "Tails"])
    await ctx.send(f"{ctx.author.mention} flipped a coin and got {a}! 🪙")
    return

# Rock, Paper, Scissors command.
@bot.command()
async def rps(ctx, choice: str):
    if ctx.guild is None:
        return
    choices = ["rock", "paper", "scissors"]
    user_choice = choice.lower()
    if user_choice not in choices:
        await ctx.send("Please choose rock, paper, or scissors.")
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
        return

@rps.error
async def rps_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please choose rock, paper, or scissors.")
        return

# Would you rather command.
@bot.command(aliases=["wyr"])
async def wouldyourather(ctx):
    if ctx.guild is None:
        return
    with open('wyr.txt', 'r') as f:
        questions = f.readlines()
    question = random.choice(questions).strip()
    file = discord.File("images/wyr.png", filename="wyr.png")
    embed = discord.Embed(title="Would You Rather", description=question)
    embed.set_thumbnail(url="attachment://wyr.png")
    await ctx.send(embed=embed, file=file)
    return

#Quote command.
@bot.command()
async def quote(ctx):
    if ctx.guild is None:
        return
    with open('quotes.txt', 'r') as f:
        quotes = f.readlines()
    quote = random.choice(quotes).strip()
    await ctx.send(f"{quote}")
    return

# Meme command.
@bot.command()
async def meme(ctx):
    if ctx.guild is None:
        return
    memeApi = urllib.request.urlopen('https://meme-api.com/gimme')
    memeData = json.load(memeApi)
    memeUrl = memeData['url']
    memeName = memeData['title']
    memePoster = memeData['author']
    embed = discord.Embed(title=memeName)  
    embed.set_image(url=memeUrl)
    await ctx.send(embed=embed)
    return

# Guess the number command.
@bot.command()
async def guess(ctx, number: int):
    if ctx.guild is None:
        return
    if not 1 <= number <= 10:
        await ctx.send("Please guess a number between 1 and 10.")
        return
    secret_number = random.randint(1, 10)
    if number is secret_number:
        await ctx.send(f"Congratulations {ctx.author.mention}! You guessed the number {secret_number}! 🎉")
    else:
        await ctx.send(f"The secret number was {secret_number}...")
        return

@guess.error
async def guess_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please guess a number between 1 and 10.")
        return

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
            return
    else:
        await ctx.send("You don't have permission to do that!")
        return

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
        return

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
    if seconds is 0:
        await ctx.send("✅ Slowmode has been disabled in this channel.")
    else:
        await ctx.send(f"✅ Slowmode set to {seconds} seconds in this channel.")
        if any(role.name in role2 for role in ctx.author.roles) is None:
            await ctx.send("You don't have permission to do that!")
            return

@slowmode.error
async def slowmode_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide a duration in seconds for slowmode. 0 to disable.")

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
                return
        else:
            await ctx.send("You need to mention a user to warn them.")
            return
    else:
        await ctx.send(f"You don't have permission to do that!")
        return

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
            return
    else:
        await ctx.send(f"You don't have permission to do that!")
        return

# Prefix command. Sets the bot's prefix.
@bot.command()
async def prefix(ctx, new_prefix: str):
    if ctx.guild is None:
        return
    if any(role.name in role2 for role in ctx.author.roles):
        bot.command_prefix = new_prefix
        await ctx.send(f"Prefix has been changed to: `{new_prefix}`")
        return
    else:
        await ctx.send("You don't have permission to do that!")
        return

@prefix.error
async def prefix_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} Please provide a new prefix.")
        return
    
bot.run(token, log_handler=handler, log_level=logging.INFO)