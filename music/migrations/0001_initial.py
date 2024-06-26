# Generated by Django 5.0.2 on 2024-03-01 18:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=200)),
                ('music', models.FileField(upload_to='musica/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discord_id', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserToSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('song_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.song')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.user')),
            ],
        ),
    ]
