# Generated by Django 3.0 on 2020-02-15 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='updateCollections',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
