# Generated by Django 3.2 on 2023-08-25 05:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinfo',
            options={'ordering': ('id',)},
        ),
    ]
