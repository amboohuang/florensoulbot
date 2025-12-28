import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime, timezone
import os
import pytz

# ======================
# Load ENV
# ======================
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1454659008530223249
ROLE_ID = 1434328186316914789
# ======================
# Intents (FIXED)
# ======================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ======================
# Timezone (UTC+7)
# ======================
tz = pytz.timezone("Asia/Bangkok")

# ======================
# Events
# ======================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    guild_hunt_reminder.start()
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
    now = datetime.now(tz)
    channel = bot.get_channel(CHANNEL_ID)

    if channel is None:
        return

    if now.weekday() in [4, 5, 6] and now.hour == 10 and now.minute == 0:
        embed = discord.Embed(
            title="⚔️ Guild Hunt Has Begun!",
            description=("**Time to bonk monsters together.**\n\n"
            "🏹 **Event Details**\n"
            "• 🗓️ **Days:** Friday, Saturday, Sunday\n"
            "• ⏰ **Time:** 10:00 – 24:00 (UTC+7)\n\n"
            "🎯 **What to Do**\n"
            "• Use all your guild hunt attempts\n"
            "• Find a group in https://discord.com/channels/1434327218498044008/1452221531814891592\n"
            "• Aim for higher rewards\n\n"
            "🏆 **No Pressure**\n"
            "Just hop in when you can and have fun."),
            color=0xE74C3C
        )

        embed.add_field(
            name="🕙 Time",
            value="10:00–24:00 (UTC+7)",
            inline=False
        )
        embed.set_thumbnail(
            url="https://external-preview.redd.it/blue-protocol-star-resonance-closed-beta-test-recruitment-v0-EmqmLnLIDdRqyK1kuBWXJ-ibeDbQLM5955mQ0sNBFDw.png?auto=webp&s=56ec719713dd3e61b2296da5de78c3f1dd220e8a")
        embed.set_footer(text="Florensoul Guild Bot")
        embed.timestamp = datetime.now(timezone.utc)

        await channel.send(
            content=f"<@&{ROLE_ID}>",
            embed=embed
        )
# ======================
# Guild Dance Reminder
# ======================
@tasks.loop(minutes=1)
async def guild_dance_reminder():
    now = datetime.now(tz)
    channel = bot.get_channel(CHANNEL_ID)

    if channel is None:
        return

    if now.weekday() == 4 and now.hour == 19 and now.minute == 30:
        embed = discord.Embed(
            title="💃 Guild Dance is Starting!",
            description="**The dance floor is open — let’s move together!**\n\n"
            "🎶 **Event Details**\n"
            "• 🗓️ **Day:** Friday\n"
            "• ⏰ **Time:** 19:30 – 19:55 (UTC+7)\n\n"
            "✨ **Why Join?**\n"
            "• Earn valuable buffs\n"
            "• Boost guild progress\n"
            "• Have fun with your guildmates\n\n"
            "🕺 **Reminder**\n"
            "Be on time — the event is short!",
            color=0x9B59B6
        )

        embed.add_field(
            name="🕢 Time",
            value="19:30 – 19:55 (UTC+7)",
            inline=False
        )

        embed.set_footer(text="Florensoul Guild Bot")
        embed.timestamp = datetime.now(timezone.utc)

        await channel.send(
            content=f"<@&{ROLE_ID}>",
            embed=embed
        )



bot.run(token)
