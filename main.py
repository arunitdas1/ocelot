import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

keep_alive()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

COGS = [
    "cogs.profile",
    "cogs.jobs",
    "cogs.banking",
    "cogs.market",
    "cogs.business",
    "cogs.stocks",
    "cogs.government",
    "cogs.indicators",
    "cogs.events_cog",
    "cogs.economy_engine",
]


@bot.event
async def on_ready():
    print(f"{bot.user} is online and the economy is running!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing argument: `{error.param.name}`. Use `!help {ctx.command}` for usage.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument type. Check `!help` for correct usage.")
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    else:
        await ctx.send(f"An error occurred: {error}")


async def load_cogs():
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"Loaded {cog}")
        except Exception as e:
            print(f"Failed to load {cog}: {e}")


@bot.event
async def setup_hook():
    await load_cogs()


bot.run(DISCORD_TOKEN)
