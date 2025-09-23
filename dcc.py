import os
import discord
from discord import app_commands
from dotenv import load_dotenv

def run_bot():
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)
    
    @client.event
    async def on_ready():
        print("[LOG] Bot is active.")
        try:
            await tree.sync()
        except Exception as e:
            print(e)

    @tree.command(name="test")
    async def test(interaction: discord.Integration):
        await interaction.response.send_message(f"Howdy {interaction.user.mention}!")
    
    client.run(TOKEN)
run_bot()