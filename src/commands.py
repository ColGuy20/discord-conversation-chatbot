import discord, logging
from discord import app_commands
import conversation as cvsn
import config as cfg

#--Contains client and commands--

def run_bot():
    # Set vars
    intents = discord.Intents.default()
    intents.message_content = True
    intents.dm_messages = True
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
        is_dm = interaction.guild is None
        cfg.log_checkpoint() # 1
        try:
            if is_dm:
                await interaction.response.send_message("Starting your session…")
            else:
                await interaction.response.defer(ephemeral=True, thinking=True)

            first_msg = await cvsn.start_session(language, profile, interaction.user.id)

            if is_dm:
                await interaction.edit_original_response(content=first_msg)
            else:
                await interaction.user.send(first_msg)
                await interaction.followup.send("Sent you a direct message!", ephemeral=True)

        except discord.Forbidden:
            text = ("I cannot send you a direct message.\nYou may have direct messages off.")
            if interaction.response.is_done():
                try:
                    if is_dm:
                        await interaction.edit_original_response(content=text)
                    else:
                        await interaction.followup.send(text, ephemeral=True)
                except Exception as e2:
                    print(f"[LOG] Forbidden fallback failed: {e2}")
            else:
                try:
                    await interaction.response.send_message(text, ephemeral=not is_dm)
                except Exception as e3:
                    print(f"[LOG] response send_message failed: {e3}")

        except Exception as e:
            print(f"[LOG] Error in /launch: {e}")
            msg = "Something went wrong starting the session."
            if interaction.response.is_done():
                try:
                    if is_dm:
                        await interaction.edit_original_response(content=msg)
                    else:
                        await interaction.followup.send(msg, ephemeral=True)
                except Exception as e2:
                    print(f"[LOG] followup/edit failed: {e2}")
            else:
                try:
                    await interaction.response.send_message(msg, ephemeral=not is_dm)
                except Exception as e3:
                    print(f"[LOG] response send_message failed: {e3}")

    # Command to end session
    @tree.command(name="end", description="End your current tutoring session.")
    async def end_cmd(interaction: discord.Interaction):
        # End the caller's session
        result = await cvsn.end_session(interaction.user.id)
        await interaction.response.send_message(result, ephemeral=True)

    #---DEV COMMANDS---

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
        print("[LOG] Bot has been shut down from discord.")
        await client.close()

    # Command to list sessions
    @tree.command(name="list", description="List sessions. (developer)")
    async def list(interaction: discord.Interaction):
        if interaction.user.id != cfg.USER_ID:
            await interaction.response.send_message(
                "You do not have permission to use this command!", ephemeral=True
            )
            return
        
        if not cfg.SESSIONS:
            session_list = "No sessions."
        else:
            lines = []
            for uid, s in cfg.SESSIONS.items():
                status = "ACTIVE" if s.active else "ENDED"
                lines.append(
                    f"- user_id={uid} | profile={s.profile.name} | lang={s.language} | "
                    f"{status} | turns={len(s.messages)}"
                )
            sessions_list = "Sessions:\n" + "\n".join(lines)
        await interaction.response.send_message(sessions_list, ephemeral=True)

    # DM message router to power the loop
    @client.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            return
        if message.guild is not None:
            return

        user_id = message.author.id
        if cvsn.has_session(user_id):
            try:
                async with message.channel.typing():
                    reply_text, _ = await cvsn.conversation(user_id, message.content)
                await message.channel.send(reply_text)
            except Exception as e:
                print(f"[LOG] on_message error for {user_id}: {e}")
                await message.channel.send("Something went wrong processing your message.")
        else:
            await message.channel.send("No active session. Use /launch to start one.")

    # Run client
    client.run(cfg.TOKEN, log_level=logging.WARNING)
