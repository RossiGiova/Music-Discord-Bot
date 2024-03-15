import discord
import os
import asyncio
import nest_asyncio
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from music.models import *
from discord.ext import commands
from audio import download_audio, get_youtube_info, search_video_url

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
TOKEN = open("token.txt", "r").readline()
nest_asyncio.apply()

songs = {}

#other

async def check_query(query:str):
    if "youtube.com" in query:
        return query
    return search_video_url(query)

#db interaction

def find_song(url):
    if Song.objects.filter(link = url).count() >= 1:
        return str(Song.objects.filter(link = url)[0].music)
    return None

async def async_find_song(url):
    if Song.objects.filter(link = url).count() >= 1:
        return str(Song.objects.filter(link = url)[0].music)
    return None

def find_url(music):
    if Song.objects.filter(music = music).count() >= 1:
        return str(Song.objects.filter(music = music)[0].link)
    return None

async def async_find_url(music):
    if Song.objects.filter(music = music).count() >= 1:
        return str(Song.objects.filter(music = music)[0].link)
    return None

def directory(title):
    return f"musica/{title}"

def save_song(url, title):
    Song(link = url, music = directory(title)).save()

def install_audio(url):
    title = download_audio(url)
    if title != None:
        save_song(url, title)
        return find_song(url)
    return None

#Queue managment

def create_queue(ctx):
    if ctx.guild.id not in songs.keys():
        songs[ctx.guild.id] = []

async def next_song(ctx):
    if len(songs[ctx.guild.id]) > 0:
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        song = songs[ctx.guild.id][0]
        songs[ctx.guild.id].pop(0)
        url = await async_find_url(song)
        asyncio.run_coroutine_threadsafe(embed_play_song(ctx, url), bot.loop)
        voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source = song), after = lambda x: asyncio.run(next_song(ctx)))

async def add_queue(ctx, url):
    song = await bot.loop.run_in_executor(None, find_song, url)
    if song == None:
        song = await bot.loop.run_in_executor(None, install_audio, url)
    if song != None:
        songs[ctx.guild.id].append(song)
        await embed_queue_song(ctx, url)

def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

#embed

async def embed_queue_song(ctx, url):
    embedBlue = 0x1976f0
    title, thumbnail, _, _ = get_youtube_info(url)
    embed = discord.Embed(
            title = "Song added to a queue",
            description = f'[{title}]({url})',
            colour = embedBlue,
        )
    embed.add_field(name="Queue Position", value=f"{len(songs[ctx.guild.id])}", inline=True)
    embed.set_thumbnail(url=thumbnail)
    await ctx.send(embed=embed)

async def embed_play_song(ctx, url):
    embedGreen = 0x0eaa51
    title, thumbnail, channel, channel_url = get_youtube_info(url)
    embed = discord.Embed(
            title = "Now playing this song",
            description = f'[{title}]({url})',
            colour = embedGreen,
        )
    embed.add_field(name="Channel", value=f"[{channel}]({channel_url})", inline=True)
    embed.set_thumbnail(url=thumbnail)
    await ctx.send(embed=embed)

async def embed_list_queue_song(ctx):
    embedpinky = 0xe505ad
    embed = discord.Embed(
            title = "Queue Position",
            colour = embedpinky,
        )
    index = 0
    if len(songs[ctx.guild.id]) > 0:
        for song in songs[ctx.guild.id]:
            index += 1
            url = find_url(song)
            title, _, _, _ = get_youtube_info(url)
            embed.add_field(name="", value=f"{index}. [{title}]({url})", inline=False)
    else:
        embed.description = "No songs left"
    await ctx.send(embed=embed)

async def embed_stop_song(ctx):
    embedyellow = 0xf7ff01
    embed = discord.Embed(
            title = "Music has been stopped",
            colour = embedyellow,
        )
    await ctx.send(embed=embed)

async def embed_resume_song(ctx):
    embedgreen = 0x0eaa51
    embed = discord.Embed(
            title = "Music has been resumed",
            colour = embedgreen,
        )
    await ctx.send(embed=embed)

async def embed_skip_song(ctx):
    embedviolet = 0xa30fc1
    embed = discord.Embed(
            title = "Skipped successfully",
            colour = embedviolet,
        )
    await ctx.send(embed=embed)

#bot function

@bot.event
async def on_ready():
    print(f'Bot was started as {bot.user.name}')

@bot.command(name='play', aliases = ["p"], help='Play song from youtbe')
async def play(ctx, *args):
    query = " ".join(args)
    if not is_connected(ctx):
        await join(ctx)
    
    url = await check_query(query)

    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if voice_client.is_playing():
        asyncio.run(add_queue(ctx, url))
    else:
        song = await bot.loop.run_in_executor(None, find_song, url)
        if song == None:
            song = await bot.loop.run_in_executor(None, install_audio, url)
        if song != None:
            await embed_play_song(ctx, url)
            voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source= song), after = lambda x: asyncio.run(next_song(ctx)))

@bot.command(name='join', aliases = ["j"], help='Join the voice channel')
async def join(ctx):
    create_queue(ctx)
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        return True
    return False

@bot.command(name='leave', aliases = ["l"], help='Left the voice channel')
async def leave(ctx):
    if is_connected(ctx):
        await ctx.guild.voice_client.disconnect()

@bot.command(name='stop', aliases = ["st"], help='Stop the player of the music bot')
async def stop(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client.is_playing():
        voice_client.pause()
        await embed_stop_song(ctx)

@bot.command(name='resume',  aliases = ["r"], help='Resume the player of the music bot')
async def resume(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client.is_paused():
        voice_client.resume()
        await embed_resume_song(ctx)

@bot.command(name = "skip",  aliases = ["s"], help="Skip the song but is playing")
async def skip(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice_client.stop()
    await embed_skip_song(ctx)

@bot.command(name = "queue", aliases = ["q"], help = "Show the Queue position")
async def queue(ctx):
    await embed_list_queue_song(ctx)

@bot.command(name = "prova", help = "prova")
async def prova(ctx):
    ...

bot.run(TOKEN)