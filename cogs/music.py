import discord
from discord import app_commands
from discord.ext import commands
import youtube_dl
import asyncio

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # Bind to IPv4 since IPv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # Take the first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='join', description='Tell the bot to join the voice channel')
    async def join(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message(f"{interaction.user.name} is not connected to a voice channel", ephemeral=True)
            return
        else:
            channel = interaction.user.voice.channel

        await channel.connect()
        await interaction.response.send_message(f"Joined {channel}", ephemeral=True)

    @app_commands.command(name='leave', description='Tell the bot to leave the voice channel')
    async def leave(self, interaction: discord.Interaction):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("Left the voice channel", ephemeral=True)
        else:
            await interaction.response.send_message("I am not in a voice channel", ephemeral=True)

    @app_commands.command(name='play', description='Play a song from a URL')
    @app_commands.describe(url='The URL of the song to play')
    async def play(self, interaction: discord.Interaction, url: str):
        async with interaction.channel.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            interaction.guild.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await interaction.response.send_message(f'Now playing: {player.title}')

    @app_commands.command(name='pause', description='Pause the currently playing song')
    async def pause(self, interaction: discord.Interaction):
        await interaction.guild.voice_client.pause()
        await interaction.response.send_message("Paused the song")

    @app_commands.command(name='resume', description='Resume the currently paused song')
    async def resume(self, interaction: discord.Interaction):
        await interaction.guild.voice_client.resume()
        await interaction.response.send_message("Resumed the song")

    @app_commands.command(name='stop', description='Stop the currently playing song')
    async def stop(self, interaction: discord.Interaction):
        await interaction.guild.voice_client.stop()
        await interaction.response.send_message("Stopped the song")

async def setup(bot):
    await bot.add_cog(Music(bot))