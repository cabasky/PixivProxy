# Generated by Django 3.0 on 2019-12-23 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artwork', '0002_auto_20191221_0735'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='Quality',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=1),
            preserve_default=False,
        ),
    ]
