# Generated by Django 2.0.3 on 2018-03-24 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Class',
            new_name='SchoolClass',
        ),
    ]
