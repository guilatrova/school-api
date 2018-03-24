# Generated by Django 2.0.3 on 2018-03-24 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0002_auto_20180324_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('correct_answer', models.PositiveSmallIntegerField(choices=[('A', 1), ('B', 2), ('C', 3), ('D', 4)])),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='quizzes.Question'),
            preserve_default=False,
        ),
    ]
