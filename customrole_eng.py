import discord, asyncio, requests
from discord import app_commands
from typing import Literal
from tree import client, tree

kafka_guild_id = 1018012987384148098

@tree.command(name="custom_role", description="Customize your own colored role! (For server boosters only)") # 슬래시 커맨드 설정에서 권한 설정해둘 것!
@app_commands.describe(name="The name of your own role")
@app_commands.describe(rgb="The RGB color code of your role. (Ignored when given with HEX) Example: `100 125 255`")
@app_commands.describe(hex="The HEX color code of your role. (Prioritized when given with RGB) Example: `FF1B42`")
@app_commands.describe(img="Whether you want to add custom image to your role")
async def customrole_eng(interaction: discord.Interaction, \
                            name: str = None, rgb: str = None, \
                            hex: str = None, img: Literal["Yes", "No"] = None):
    user = interaction.user
    username = user.name
    guild = await client.fetch_guild(kafka_guild_id)

    for role in user.roles: # 전에 만든 커스텀 역할이 있다면 삭제
        splt = role.name.split(" ৹ ")
        if len(splt) >= 2 and  splt[1] == username \
           or len(splt) == 1 and splt[0] == username: # 커스텀 역할 이름이 있는 경우와 없는 경우
            await discord.Role.delete(role)

    if not (name or rgb or hex or img): # 아무 인자의 입력도 없음
        await interaction.response.send_message("Nothing happened because you entered nothing!")
        return
    
    if name and " ৹ " in name: # 유저네임 확인을 위해 역할 이름에 " ৹ "을 넣을 수 없음
        await interaction.response.send_message("You can't include ` ৹ ` in your role name. Please try again.")
        return
    
    if not name: # name 인자 입력이 없을 경우 구분 문자가 없는 형식으로 설정
        name = username
    else:
        name = f"{name} ৹ {username}"
    
    if (rgb and hex) or (not rgb and hex): # rgb와 hex가 모두 입력되었을 경우 후자를 우선시
        try:
            color = discord.Color.from_str(f"#{hex}") # 입력 시 # 안 붙여야함!
        except ValueError:
            await interaction.response.send_message("You should enter HEX color code (without #) in `hex` parameter!")
            return
    elif rgb and not hex:
        try:
            r, g, b = int(rgb.split()[0]), int(rgb.split()[1]), int(rgb.split()[2])
            color = discord.Color.from_rgb(r, g, b)
        except ValueError:
            await interaction.response.send_message("You should enter 3 natural integers (0~255) seperated with spaces in `rgb` parameter!")
            return
    else:
        color = discord.Color.default()

    if img == "Yes":
        await interaction.response.send_message(
            f"{user.mention} The first image you upload to this channel in \
1 minutes from now on will be your role's icon. PNG or JPEG image file only!")
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
            await interaction.channel.send(f"{new_role.mention} Your custom role has been sucessfully applied!")
        except asyncio.TimeoutError:
            await interaction.channel.send(f"{user.mention} Your custom role registration has been cancelled.")
        except ValueError:
            await interaction.channel.send(f"{user.mention} **PNG or JPEG image file only!**\nYour custom role registration has been cancelled.")
            
    else:
        new_role = await guild.create_role(name=name, color=color, hoist=True)
        await guild.edit_role_positions({new_role: 10})
        await user.add_roles(new_role)
        await interaction.response.send_message(f"{new_role.mention} Your custom role has been sucessfully applied!")