import discord

from tree import client, tree

async def get_guild_info():
    global art_guild, check_role, uploaded_role, notif_role, \
    log, feedback, finished_art, wip_n_rkgk
    art_guild = discord.utils.get(client.guilds, id=1018012987384148098)
    check_role = discord.utils.get(art_guild.roles, id=1125561855822286899)
    uploaded_role = discord.utils.get(art_guild.roles, id=1125772994103496847)
    notif_role = discord.utils.get(art_guild.roles, id=1126285702276071555)
    log = discord.utils.get(art_guild.text_channels, id=1036516805793030175)
    feedback = discord.utils.get(art_guild.forums, id=1044297846129700904)
    finished_art = discord.utils.get(art_guild.text_channels, id=1030729942050291722)
    wip_n_rkgk = discord.utils.get(art_guild.text_channels, id=1030724720808702012)


def check_but_not_uploaded(member: discord.Member):
    return check_role in member.roles and uploaded_role not in member.roles

def uploaded_in_art_channel(msg: discord.Message):
    return msg.channel == finished_art or msg.channel == wip_n_rkgk

def uploaded_in_feedback_forum(thread: discord.Thread):
    return thread.parent == feedback

def msg_contains_img(msg: discord.Message):
    return msg.attachments != [] or msg.content.startswith("https://twitter.com/") \
           or msg.content.startswith("https://vxtwitter.com/")


@tree.command(name="멘션용_역할부여", description="그림을 업로드하지 않은 멤버들에게 역할을 일괄 부여합니다.")
async def give_ping_roles(interaction: discord.Interaction):
    await interaction.response.send_message("역할을 부여하는 중입니다…")

    notif_role_initial = len(notif_role.members)
    for member in check_role.members:
        if uploaded_role not in member.roles:
            await member.add_roles(notif_role)
    notif_role_final = len(notif_role.members)
    count = notif_role_final - notif_role_initial
    await interaction.channel.send(f"{count}명의 멤버에게 역할 부여가 완료되었습니다!")

    # 월 초의 일괄 제거는 dyno를 사용할 것

async def check_art_upload(msg: discord.Message):
    if uploaded_in_art_channel(msg) and msg_contains_img(msg):
        await msg.add_reaction("❤️")
        if check_but_not_uploaded(msg.author):
            await log.send(f"<@{msg.author.id}>님이 그림을 업로드했습니다. 해당 멤버에게 인증 역할을 부여합니다...")
            try:
                await msg.author.add_roles(uploaded_role)
                await log.send("성공적으로 역할을 부여했습니다.")
                if notif_role in msg.author.roles:
                    await msg.author.remove_roles(notif_role)
                    await log.send(f"또한, <@{msg.author.id}>님에게서 업로드 알림용 역할을 제거했습니다.")
            except:
                await log.send("<@513676568745213953> 문제가 발생했습니다. 에러 로그를 확인하세요.")


async def check_feedback_upload(thread: discord.Thread):
    try:
        starter_message = await thread.fetch_message(thread.id)
    except:
        return
    if check_but_not_uploaded(thread.owner) and uploaded_in_feedback_forum(thread) and msg_contains_img(starter_message):
        await log.send(f"<@{thread.owner_id}>님이 그림을 업로드했습니다. 해당 멤버에게 인증 역할을 부여합니다...")
        try:
            await starter_message.author.add_roles(uploaded_role)
            await log.send("성공적으로 역할을 부여했습니다.")
            if notif_role in starter_message.author.roles:
                await starter_message.author.remove_roles(notif_role)
                await log.send(f"또한, <@{starter_message.author.id}>님에게서 업로드 알림용 역할을 제거했습니다.")
        except:
            await log.send("<@513676568745213953> 문제가 발생했습니다. 에러 로그를 확인하세요.")