# Generated by Django 2.0.3 on 2018-03-25 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0010_auto_20180325_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='grade',
            field=models.IntegerField(default=0),
        ),
    ]
