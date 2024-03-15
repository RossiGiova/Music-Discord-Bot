# Music-Discord-Bot

# How to install

You have to install on your computer Python 3.x and these libraries with the command below
```
pip install discord django nest-asyncio pytube PyNaCl ffmpeg
```
you have to add to token

First on `db/django_key.txt` where you add your django secret key

Second on `token.txt` where you add your discord bot token

and then you have to create a database with django.

finally check you have installed the program ffmpeg from www.ffmpeg.org and change the executable path from `music_bot.py`

Now you can run the from the file `music_bot.py`

# Bot commands

```
!play <link on youtube or sometext>
```
Search the music save it on the database and after bot play it on the voice chat, if the bot is playing a song he add the song to a queue
```
!queue 
```
Show the queue of song bot have to play
```
!join
```
Discord bot join the voice channel
```
!leave
```
Discord bot leave the voice channel
```
!stop
```
if bot is playing a song he stop
```
!resume
```
if bot was stopped while playing a song, he resume
```
!skip
```
Discord bot go on the next song in the queue
