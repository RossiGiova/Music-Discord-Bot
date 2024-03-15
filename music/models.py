from django.db import models

class User(models.Model):
    discord_id = models.CharField(max_length = 200, unique = True)

class Song(models.Model):
    link = models.CharField(max_length = 200, unique = True)
    music = models.FileField(upload_to="musica/")

class UserToSong(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200, unique = True)
