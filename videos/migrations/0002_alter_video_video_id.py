# Generated by Django 4.2.9 on 2024-02-03 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_id',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
