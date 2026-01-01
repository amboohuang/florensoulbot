import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime, timezone
import os
import pytz
import webserver

# ======================
# Load ENV
# ======================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

CHANNEL_ID = 1454659008530223249
ROLE_ID = 1434328186316914789

# ======================
# Intents
# ======================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ======================
# Timezone (UTC+7)
# ======================
tz = pytz.timezone("Asia/Bangkok")

# ======================
# Anti-duplicate guards
# ======================
last_hunt_sent = None
last_dance_sent = None

# ======================
# Events
# ======================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    if not guild_hunt_reminder.is_running():
        guild_hunt_reminder.start()

    if not guild_dance_reminder.is_running():
        guild_dance_reminder.start()

# ======================
# Commands
# ======================
@bot.command()
async def test(ctx):
    await ctx.send("🧪 **Bot is working in this channel!**")

# ======================
# Guild Hunt Reminder
# ======================
@tasks.loop(minutes=1)
async def guild_hunt_reminder():
    global last_hunt_sent

    now = datetime.now(tz)
    today = now.date()

    if last_hunt_sent == today:
        return

    if now.weekday() in [4, 5, 6] and now.hour == 10 and now.minute == 0:
        channel = bot.get_channel(CHANNEL_ID)
        if channel is None:
            return

        embed = discord.Embed(
            title="⚔️ Guild Hunt Has Begun!",
            description=(
                "**Time to bonk monsters together.**\n\n"
                "🏹 **Event Details**\n"
                "• 🗓️ **Days:** Friday, Saturday, Sunday\n"
                "• ⏰ **Time:** 10:00 – 24:00 (UTC+7)\n\n"
                "🎯 **What to Do**\n"
                "• Use all your guild hunt attempts\n"
                "• Find a group in the party finder channel\n"
                "• Aim for higher rewards\n\n"
                "🏆 **No Pressure**\n"
                "Just hop in when you can and have fun."
            ),
            color=0xE74C3C
        )

        embed.set_thumbnail(
            url="https://external-preview.redd.it/blue-protocol-star-resonance-closed-beta-test-recruitment-v0-EmqmLnLIDdRqyK1kuBWXJ-ibeDbQLM5955mQ0sNBFDw.png"
        )
        embed.set_footer(text="Florensoul Guild Bot")
        embed.timestamp = datetime.now(timezone.utc)

        await channel.send(
            content=f"<@&{ROLE_ID}>",
            embed=embed
        )

        last_hunt_sent = today
        print("⚔️ Guild Hunt reminder sent")

@guild_hunt_reminder.before_loop
async def before_hunt():
    await bot.wait_until_ready()

# ======================
# Guild Dance Reminder
# ======================
@tasks.loop(minutes=1)
async def guild_dance_reminder():
    global last_dance_sent

    now = datetime.now(tz)
    today = now.date()

    if last_dance_sent == today:
        return

    if now.weekday() == 4 and now.hour == 19 and now.minute == 30:
        channel = bot.get_channel(CHANNEL_ID)
        if channel is None:
            return

        embed = discord.Embed(
            title="💃 Guild Dance is Starting!",
            description=(
                "**The dance floor is open — let’s move together!**\n\n"
                "🎶 **Event Details**\n"
                "• 🗓️ **Day:** Friday\n"
                "• ⏰ **Time:** 19:30 – 19:55 (UTC+7)\n\n"
                "✨ **Why Join?**\n"
                "• Earn valuable buffs\n"
                "• Boost guild progress\n"
                "• Have fun with your guildmates\n\n"
                "🕺 **Reminder**\n"
                "Be on time — the event is short!"
            ),
            color=0x9B59B6
        )

        embed.set_footer(text="Florensoul Guild Bot")
        embed.timestamp = datetime.now(timezone.utc)

        await channel.send(
            content=f"<@&{ROLE_ID}>",
            embed=embed
        )

        last_dance_sent = today
        print("💃 Guild Dance reminder sent")

@guild_dance_reminder.before_loop
async def before_dance():
    await bot.wait_until_ready()

# ======================
# Webserver (Render keep-alive)
# ======================
webserver.keep_alive()

# ======================
# Run bot
# ======================
bot.run(TOKEN)
