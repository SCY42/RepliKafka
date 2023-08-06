import discord, os
from dotenv import load_dotenv

from tree import client, tree
from customrole_eng import customrole_eng
from customrole_kor import customrole_kor
from suggestionbox import SuggestionBoxView, suggestionbox
from uploadcheck_autoreact import get_guild_info, give_ping_roles, check_art_upload, check_feedback_upload

# commands = [customrole_eng, customrole_kor, suggestionbox, give_ping_roles]
# for command in commands:
#     tree.add_command(command)

@client.event
async def on_ready():
    print(f"Loading Guild Info ...")
    await tree.sync()
    await get_guild_info()
    client.add_view(SuggestionBoxView())
    print(f"The Bot is Ready!")

@client.event
async def on_message(msg: discord.Message):
    if msg.author == client.user:
        return
    await check_art_upload(msg)

@client.event
async def on_thread_create(thread: discord.Thread):
    if thread.owner == client.user:
        return
    await check_feedback_upload(thread)
    
@tree.command(name="핑")
async def ping_kor(interaction: discord.Interaction):
    await interaction.response.send_message(f"현재 핑은 {round(client.latency*1000)}ms 입니다.")

@tree.command(name="ping")
async def ping_eng(interaction: discord.Interaction):
    await interaction.response.send_message(f"Current Latency is {round(client.latency*1000)}ms.")

load_dotenv()
replikafka_token = os.getenv("replikafka_token")
client.run(replikafka_token)