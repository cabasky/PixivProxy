# Generated by Django 3.0 on 2019-12-28 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artwork', '0007_auto_20191227_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='imgformat',
            field=models.IntegerField(choices=[(0, 'jpg'), (1, 'png')], default=0),
            preserve_default=False,
        ),
    ]