import discord
import os
import sys
from discord.ext import commands
import random
import datetime
import requests
from io import BytesIO
import platform
import asyncio
from discord import app_commands, ui
import time


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class client(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = None)
            self.synced = True
        self.start_time = datetime.datetime.now()  # Set start_time here
        print('Bot online.')
        await aclient.change_presence(status=discord.Status.online, activity=discord.Game('use /cmd to get started!'))
aclient = client()
tree = app_commands.CommandTree(aclient)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(guild=None, name='cmd', description='shows the list of commands!')
async def cmd(interaction: discord.Interaction):
  embed = discord.Embed(title="here are my commands!", description="Here are the available commands:")     # cmd
  embed.add_field(name="`serverinfo`", value="shows info on the server!", inline=False)
  embed.add_field(name="`userinfo`", value="shows info on the mentioned user!", inline=False)
  embed.add_field(name="`uptime`", value="displays the bot uptime!", inline=False)
  embed.add_field(name="`avatar`", value="shows the mentioned users PFP!", inline=False)
  embed.add_field(name="`calc`", value="calcuate something!", inline=False)
  embed.add_field(name="`ping`", value="shows the bot latency!", inline=False)
  embed.add_field(name="`cat`", value="shows a random cat picture!", inline=False)
  embed.add_field(name="`roll`", value="roll a random number 1-10!", inline=False)
  embed.add_field(name="`rps`", value="play rock paper sissors!", inline=False)
  embed.add_field(name="`coinflip`", value="flip a coin!", inline=False)
  await interaction.response.send_message(embed=embed, ephemeral=True)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(guild=None, name='modcmd', description='shows the list of commands for moderators!')
@commands.has_permissions(manage_messages=True)
async def cmd(interaction: discord.Interaction):
    if not interaction.channel.permissions_for(interaction.user).manage_messages:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return
    embed = discord.Embed(title="here are mod commands!", description="Here are the available commands: ")
    embed.add_field(name="`ban`", value="bans a user!", inline=False)
    embed.add_field(name="`unban`", value="unbans a user! (userID)", inline=False)
    embed.add_field(name="`purge`", value="dclears a set amount of messages! (1-100)", inline=False)
    embed.add_field(name="`say`", value="makes the bot say something!", inline=False)
    embed.add_field(name="`addrole`", value="adds a role to the mentioned user!", inline=False)
    embed.add_field(name="`poll`", value="makes a poll!", inline=False)
    embed.add_field(name="`lock`", value="locks the current channel!", inline=False)
    embed.add_field(name="`unlock`", value="unlocks the current channel!", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name='serverinfo', description='Get information about the server!')
@commands.cooldown(1, 10, commands.BucketType.user)
async def serverinfo(interaction: discord.Interaction):
    server = interaction.guild
    embed = discord.Embed(title='Server Information', color=discord.Color.blue())
    embed.add_field(name='`Server Name - 🏠`', value=server.name, inline=False)                  # server info
    embed.add_field(name='`Server ID - 📊`', value=server.id, inline=False)
    embed.add_field(name='`Member Count - 👥`', value=server.member_count, inline=False)
    embed.add_field(name='`Created at - 📆`', value=server.created_at, inline=False)
    embed.add_field(name='`Owner - 👑`', value=server.owner, inline=False)
    await interaction.response.send_message(embed=embed)


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name='userinfo', description='Get information about the mentioned user')
@commands.cooldown(1, 10, commands.BucketType.user)
async def userinfo(interaction: discord.Interaction, user: discord.Member = None):
    if user is None:
        user = interaction.user
    embed = discord.Embed(title='User Information', color=discord.Color.blue())
    embed.set_thumbnail(url=user.avatar.url)
    embed.add_field(name='`User Name - 👤`', value=user.name, inline=False)                    # userinfo
    embed.add_field(name='`User ID - 📊`', value=user.id, inline=False)
    embed.add_field(name='`Created at - 📆`', value=user.created_at, inline=False)
    embed.add_field(name='`Joined at - 📅`', value=user.joined_at, inline=False)
    embed.add_field(name='`Roles - 👑`', value=', '.join([role.name for role in user.roles][1:]), inline=False)
    await interaction.response.send_message(embed=embed)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name='uptime', description='Displays the bot uptime')
async def uptime(interaction: discord.Interaction):
    uptime = datetime.datetime.now() - aclient.start_time
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)          # uptime
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    embed = discord.Embed(title='Uptime', description=f'the bot has been running for: \n\n `{days} days, {hours} hours, {minutes} minutes, {seconds} seconds`', color=discord.Color.blue())
    await interaction.response.send_message(embed=embed)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\

@tree.command(name='say', description='Makes the bot say a message')
@commands.has_permissions(administrator=True)
async def say(interaction: discord.Interaction, message: str):
    if not interaction.channel.permissions_for(interaction.user).administrator:
        await interaction.response.send_message('You do not have permission to use this command.', ephemeral=True)  # say
        return
    await interaction.response.send_message(message)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name='purge', description='Deletes a specified number of messages')
@commands.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, limit: int):
    if not interaction.channel.permissions_for(interaction.user).manage_messages:
        await interaction.response.send_message('You do not have permission to use this command.', ephemeral=True)
        return
    await interaction.response.defer()                                   # purge
    await interaction.channel.purge(limit=limit)
    embed = discord.Embed(title='Purge Complete', description=f'Deleted {limit} messages.', color=discord.Color.green())
    msg = await interaction.channel.send(embed=embed)
    await asyncio.sleep(10)
    await msg.delete()

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name="unlock", description="Unlocks the current channel!")
async def unlock_channel(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.manage_channels:
        embed = discord.Embed(title="Error", description="You do not have the `Manage Channels` permission.", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    channel = interaction.channel
    overwrite = channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = None
    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    embed = discord.Embed(title="Channel Unlocked", description=f"Channel unlocked by {interaction.user.mention}!", color=0x00FF00)
    await interaction.response.send_message(embed=embed)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name="lock", description="Locks the current channel!")
@commands.has_permissions(manage_channels=True)
async def lock_channel(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.manage_channels:
        embed = discord.Embed(title="Error", description="You don't have the `Manage Channels` permission!", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    channel = interaction.channel
    overwrite = channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    embed = discord.Embed(title="Channel Locked", description=f"Channel locked by {interaction.user.mention}!", color=0x00FF00)
    await interaction.response.send_message(embed=embed)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name='unban', description='Unbans a user')
@commands.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, user_id: str):
    if not interaction.channel.permissions_for(interaction.user).ban_members:
        await interaction.response.send_message('You do not have permission to use this command.', ephemeral=True)
        return
    await interaction.response.defer()
    try:
        user_id = int(user_id)
    except ValueError:
        await interaction.followup.send('Please input a valid user ID.', ephemeral=True)
        return
    try:
        ban_entry = await interaction.guild.fetch_ban(discord.Object(id=user_id))
        await interaction.guild.unban(ban_entry.user)
        embed = discord.Embed(title='User Unbanned', description=f'User with ID `{user_id}` has been unbanned.', color=discord.Color.green())
        await interaction.followup.send(embed=embed)
    except discord.NotFound:
        await interaction.followup.send('User not found or not banned.', ephemeral=True)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name='ban', description='Bans a user')
@commands.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str = None):
    if not interaction.channel.permissions_for(interaction.user).ban_members:
        await interaction.response.send_message('You do not have permission to use this command.', ephemeral=True)
        return
    await interaction.response.defer()
    await user.ban(reason=reason)
    embed = discord.Embed(title='User Banned', description=f'{user.mention} has been banned.', color=discord.Color.red())
    if reason:
        embed.add_field(name='Reason', value=reason, inline=False)
    await interaction.followup.send(embed=embed)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name='addrole', description='Adds a role to a member')
@commands.has_permissions(manage_roles=True)
async def addrole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if not interaction.channel.permissions_for(interaction.user).manage_roles:
        await interaction.response.send_message('You do not have permission to use this command.', ephemeral=True)
        return
    await interaction.response.defer()
    if role.position >= interaction.guild.me.top_role.position:
        await interaction.followup.send('I cannot add that role as it is higher than my highest role.', ephemeral=True)
        return
    await member.add_roles(role)
    embed = discord.Embed(title='Role Added', description=f'{member.mention} has been given the role {role.mention}', color=discord.Color.green())
    await interaction.followup.send(embed=embed)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name='cat', description='Shows a random picture of a cat!')
async def cat(interaction: discord.Interaction):
    await interaction.response.defer()
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    data = response.json()
    embed = discord.Embed(title='Heres a random cat picture!', color=discord.Color.blue())
    embed.set_image(url=data[0]['url'])
    await interaction.followup.send(embed=embed)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name='calc', description='Calculates equations!')
async def calculate(interaction: discord.Interaction, operation: str, num1: float, num2: float):
    await interaction.response.defer()
    if operation == 'add':
        result = num1 + num2
    elif operation == 'subtract':
        result = num1 - num2
    elif operation == 'multiply':
        result = num1 * num2
    elif operation == 'divide':
        if num2 != 0:
            result = num1 / num2
        else:
            await interaction.followup.send('Error: Division by zero is not allowed.')
            return
    else:
        await interaction.followup.send('Error: Invalid operation. Please use "add", "subtract", "multiply", or "divide".')
        return
    embed = discord.Embed(title='Calculation Result', description=f'{num1} {operation} {num2} = {result}', color=discord.Color.green())
    await interaction.followup.send(embed=embed)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name='roll', description='Rolls a random number between 1 and 10')
async def roll(interaction: discord.Interaction):
    await interaction.response.defer()
    result = random.randint(1, 10)
    embed = discord.Embed(title='Roll Result', description=f'You rolled a {result}', color=discord.Color.green())
    await interaction.followup.send(embed=embed)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name='coinflip', description='Flips a coin!')
async def flip(interaction: discord.Interaction):
    await interaction.response.defer()
    result = random.choice(['Heads', 'Tails'])
    embed = discord.Embed(title='Coin Flip Result', description=f'You flipped a {result}!', color=discord.Color.green())
    await interaction.followup.send(embed=embed)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name='ping', description='Shows the bots latency!')
async def ping(interaction: discord.Interaction):
    await interaction.response.defer()
    latency = interaction.client.latency * 1000
    embed = discord.Embed(title='Pong!', description=f'The bots latency is {latency:.2f}ms.', color=discord.Color.green())
    await interaction.followup.send(embed=embed)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name='rps', description='Play Rock Paper Scissors')
async def rps(interaction: discord.Interaction, choice: str):
    choices = ['rock', 'paper', 'scissors']
    if choice.lower() not in choices:
        await interaction.response.send_message('Invalid choice. Please choose "rock", "paper", or "scissors".', ephemeral=True)
        return
    bot_choice = random.choice(choices)
    if choice.lower() == bot_choice:
        result = 'It\'s a tie!'
    elif (choice.lower() == 'rock' and bot_choice == 'scissors') or (choice.lower() == 'paper' and bot_choice == 'rock') or (choice.lower() == 'scissors' and bot_choice == 'paper'):
        result = 'You win!'
    else:
        result = 'You lose!'
    embed = discord.Embed(title='Rock Paper Scissors', description=f'You chose {choice.lower()}, I chose {bot_choice}. {result}', color=discord.Color.green())
    await interaction.response.send_message(embed=embed, ephemeral=True)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name='avatar', description='Copies the avatar of the mentioned user')
async def avatar(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()
    embed = discord.Embed(title=f'{user.name}\'s Avatar', color=discord.Color.blue())
    embed.set_image(url=user.display_avatar.url)
    await interaction.followup.send(embed=embed)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

EMOJI_NUMBERS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

@tree.command(name='poll', description='Creates a poll')
@commands.has_permissions(administrator=True)
async def poll(interaction: discord.Interaction, question: str, option1: str, option2: str, option3: str = None, option4: str = None, option5: str = None):
    await interaction.response.defer()
    options = [option1, option2]
    if option3:
        options.append(option3)
    if option4:
        options.append(option4)
    if option5:
        options.append(option5)
    embed = discord.Embed(title=question, description='React to vote', color=discord.Color.blue())
    for i, option in enumerate(options):
        embed.add_field(name=f'Option {i+1}', value=option, inline=False)
    message = await interaction.channel.send(embed=embed)
    for i in range(len(options)):
        await message.add_reaction(EMOJI_NUMBERS[i])
    await interaction.followup.send('`POLL`')

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@tree.command(name='8ball', description='Ask the magic 8 ball a question')
async def eight_ball(interaction: discord.Interaction, question: str):
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes, definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "No.",
        "Better not tell you now.",
        "Nah, don't even think about it.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]

    embed = discord.Embed(title='8 Ball result', description=f'Question: {question}\nAnswer: {random.choice(responses)}', color=discord.Color.blue())
    await interaction.response.send_message(embed=embed)
    


aclient.run('your token here.')

