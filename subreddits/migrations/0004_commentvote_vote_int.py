# Generated by Django 3.0.8 on 2020-07-23 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subreddits', '0003_auto_20200723_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentvote',
            name='vote_int',
            field=models.IntegerField(default=0),
        ),
    ]
