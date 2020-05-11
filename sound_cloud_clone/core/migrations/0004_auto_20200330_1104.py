# Generated by Django 3.0 on 2020-03-30 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_album_artist_of_album'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='album',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='song',
        ),
        migrations.AddField(
            model_name='album',
            name='artist_of_album',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Artist'),
        ),
        migrations.AddField(
            model_name='song',
            name='artist_of_song',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Artist'),
        ),
    ]
