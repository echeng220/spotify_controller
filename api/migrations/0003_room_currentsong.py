# Generated by Django 4.1.3 on 2022-11-28 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_rename_created_at_room_createdat_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="currentSong",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
