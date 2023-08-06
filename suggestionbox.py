import discord
from tree import client

class MyModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="서버 비공개 건의함 | Private Suggestion Box", timeout=None, custom_id="suggestionbox_modal_persistent")
    suggtitle = discord.ui.TextInput(label="건의 제목 | Title of Suggestion", style=discord.TextStyle.short, \
                         placeholder="건의 사항의 간단한 요약 | A short summary of the suggestion")
    suggestion = discord.ui.TextInput(label="건의 내용 | Content of Suggestion", style=discord.TextStyle.paragraph, \
                              placeholder="운영진에게 전하고 싶은 말 | What you want to suggest to the staff")
    async def on_submit(self, interaction: discord.Interaction):
        content_channel = await client.fetch_channel(1127395888449474610)
        embed = discord.Embed(title=self.suggtitle, description=self.suggestion)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="건의자 정보", value=f"<@{interaction.user.id}>")
        await content_channel.send(embed=embed)
        await interaction.response.send_message("감사합니다! | Thank You!", ephemeral=True)


class SuggestionBoxView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)   

    @discord.ui.button(emoji="📜", label="서버 운영진에게 건의 보내기 | Send a suggestion to server staffs", style=discord.ButtonStyle.blurple, custom_id="suggestionbox_button_persistent")
    async def callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(MyModal())


async def suggestionbox():
    suggestion_channel = await client.fetch_channel(1127740115838582815)
    embedcontent = ":white_small_square:더 효율적인 건의사항 관리를 위한 건의함입니다. 아래의 버튼을 눌러 운영진에게만 공개되는 건의사항을 전송하세요. \
**건의는 익명으로 전송되지 않으며**, 불쾌하거나 모욕적인 내용이 포함되어 있을 경우 본 서버에서의 활동에 제재를 받으실 수 있습니다.\n\
:white_small_square:건의 전송에 실패했을 경우, 봇에 이상이 있는 상황일 수 있으니 <@513676568745213953>를 멘션해 알려 주세요.\n\
:white_small_square:본인의 그림이 NSFW로 분류되는지 확인받고 싶으신 경우, <@289968032527155200>에게 DM으로 질문하세요.\n\
:white_small_square:그 외 부득이한 경우를 제외하고는, 건의사항을 운영진에게 직접 보내는 것은 삼가 주시기 바랍니다.\n\n\
:white_small_square:An update to the format of the suggestions box for improved efficacy. \
Press this button to send a suggestion to the staff, which contents will not be visible to non-staff. \
Note, **the suggestions will not be sent anonymously**, and using this tool to harass the staff may result in penalties.\n\
:white_small_square:If the suggestion fails to send, this may indicate a problem with the bot handling it: Please mention <@513676568745213953> to get this resolved.\n\
:white_small_square:For the purpose of inquiring if a potential upload would satisfy the NSFW guidelines, please DM <@289968032527155200> directly.\n\
:white_small_square:Outside of extraordinary circumstances, please refrain from sending the suggestions directly to a specific staff member."
    embed = discord.Embed(title="서버 비공개 건의함 | Private Suggestions Box", description=embedcontent)
    view = SuggestionBoxView()
    await suggestion_channel.send(embed=embed, view=view)