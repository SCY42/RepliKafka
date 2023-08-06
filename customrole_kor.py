import discord, asyncio, requests
from discord import app_commands
from typing import Literal
from tree import client, tree

kafka_guild_id = 1018012987384148098

@tree.command(name="커스텀_역할", description="자신만의 색상 역할을 만들어보세요! (서버 부스터만 가능)") # 슬래시 커맨드 설정에서 권한 설정해둘 것!
@app_commands.describe(name="역할의 이름")
@app_commands.describe(rgb="역할의 RGB 컬러 코드. (HEX와 동시에 입력했을 시 무시됨) 예시: `100 125 255`")
@app_commands.describe(hex="역할의 HEX 컬러 코드. (RGB와 동시에 입력했을 시 우선시됨) Example: `FF1B42`")
@app_commands.describe(img="커스텀 역할 아이콘을 넣을지 여부")
async def customrole_kor(interaction: discord.Interaction, \
                            name: str = None, rgb: str = None, \
                            hex: str = None, img: Literal["네", "아니요"] = None):
    user = interaction.user
    username = user.name
    guild = await client.fetch_guild(kafka_guild_id)

    for role in user.roles: # 전에 만든 커스텀 역할이 있다면 삭제
        splt = role.name.split(" ৹ ")
        if len(splt) >= 2 and  splt[1] == username \
           or len(splt) == 1 and splt[0] == username: # 커스텀 역할 이름이 있는 경우와 없는 경우
            await discord.Role.delete(role)

    if not (name or rgb or hex or img): # 아무 인자의 입력도 없음
        await interaction.response.send_message("아무 것도 입력하지 않으셨으므로, 아무 일도 일어나지 않았습니다!")
        return
    
    if name and " ৹ " in name: # 유저네임 확인을 위해 역할 이름에 " ৹ "을 넣을 수 없음
        await interaction.response.send_message("역할 이름에는 ` ৹ `를 포함시킬 수 없습니다. 다시 시도해주세요.")
        return
    
    if not name: # name 인자 입력이 없을 경우 구분 문자가 없는 형식으로 설정
        name = username
    else:
        name = f"{name} ৹ {username}"
    
    if (rgb and hex) or (not rgb and hex): # rgb와 hex가 모두 입력되었을 경우 후자를 우선시
        try:
            color = discord.Color.from_str(f"#{hex}") # 입력 시 # 안 붙여야함!
        except ValueError:
            await interaction.response.send_message("`hex` 항목에는 (#를 뺀) HEX 컬러 코드를 입력하셔야 합니다!")
            return
    elif rgb and not hex:
        try:
            r, g, b = int(rgb.split()[0]), int(rgb.split()[1]), int(rgb.split()[2])
            color = discord.Color.from_rgb(r, g, b)
        except ValueError:
            await interaction.response.send_message("`rgb` 항목에는 띄어쓰기로 구분된 3개의 자연수 (0~255) 를 입력하셔야 합니다!")
            return
    else:
        color = discord.Color.default()

    if img == "네":
        await interaction.response.send_message(
            f"{user.mention} 지금부터 1분 이내에 처음으로 이 채널에 업로드하시는 이미지가 커스텀 역할의 아이콘이 됩니다.\
 PNG 또는 JPEG 이미지 파일만 가능합니다!")
        def check(msg: discord.Message):
            return msg.author == user and msg.channel == interaction.channel and msg.attachments != []
        try:
            message = await client.wait_for("message", check=check, timeout=60)
            img_url = message.attachments[0].url
            response = requests.get(img_url)
            img = response.content
            new_role = await guild.create_role(name=name, color=color, display_icon=img, hoist=True)

            await guild.edit_role_positions({new_role: 10})
            await user.add_roles(new_role)
            await interaction.channel.send(f"{new_role.mention} 커스텀 역할이 성공적으로 적용되었습니다!")
        except asyncio.TimeoutError:
            await interaction.channel.send(f"{user.mention} 커스텀 역할 등록이 취소되었습니다.")
        except ValueError:
            await interaction.channel.send(f"{user.mention} **PNG 또는 JPEG 이미지 파일만 가능합니다!**\n커스텀 역할 등록이 취소되었습니다.")
            
    else:
        new_role = await guild.create_role(name=name, color=color, hoist=True)
        await guild.edit_role_positions({new_role: 10})
        await user.add_roles(new_role)
        await interaction.response.send_message(f"{new_role.mention} 커스텀 역할이 성공적으로 적용되었습니다!")