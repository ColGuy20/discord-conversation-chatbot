import discord
import conversation as cvsn
import config as cfg
from discord import app_commands

def run_bot():
    # Set vars
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    # Start and sync bot
    @client.event
    async def on_ready():
        print("[LOG] Bot is active.")
        try:
            await tree.sync()
            print("[LOG] Bot is synched globally.")
        except Exception as e:
            print(f"[LOG] Global sync failed: {e}")

    # Command to initiate session
    @tree.command(name="launch", description="Initiate the chat session.")
    @app_commands.describe(language="Language to use", profile="Profile to speak with")
    @app_commands.choices(
        language=[app_commands.Choice(name=l, value=l) for l in cfg.lang_array], 
        profile=[app_commands.Choice(name=p, value=p) for p in cfg.list_profile_names()]
        )
    async def launch(interaction: discord.Interaction, language: str, profile: str):
        try:
            await interaction.response.send_message(
                f"Sent you a direct message!", 
                ephemeral=True
            )
            cvsn.conversation_start(language, profile)

        except discord.Forbidden:
            await interaction.response.send_message(
                "I cannot send a direct message to you. You may have direct messages off.",
                ephemeral=True
            )

    # Command to directly sync from discord
    @tree.command(name="sync", description="Sync app commands (developer)")
    async def sync(interaction: discord.Interaction):
        if interaction.user.id != cfg.USER_ID:
            await interaction.response.send_message(
                "You do not have permission to use this command!", ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True, thinking=True)
        print("[LOG] Attempt to sync from discord.")

        try:
            synced = await tree.sync()
            await interaction.followup.send(
                f"The bot is synched. ({len(synced)} commands).",
                ephemeral=True
            )
            print("[LOG] Bot synced from discord.")
        except Exception as e:
            await interaction.followup.send("Sync failed. Check logs.", ephemeral=True)
            print(f"[LOG] Sync from discord failed.\n{e}")

    # Command to end program from discord
    @tree.command(name="terminate", description="Terminate program. (developer)")
    async def terminate(interaction: discord.Interaction):
        if interaction.user.id != cfg.USER_ID:
            await interaction.response.send_message(
                "You do not have permission to use this command!", ephemeral=True
            )
            return
        await interaction.response.send_message("Shutting down…", ephemeral=True)
        await client.close()

    # Run client
    client.run(cfg.TOKEN)
