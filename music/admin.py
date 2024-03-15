from django.contrib import admin
from .models import User, UserToSong, Song
# Register your models here.

admin.site.register(User)
admin.site.register(UserToSong)
admin.site.register(Song)
