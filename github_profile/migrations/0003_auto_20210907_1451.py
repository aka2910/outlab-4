# Generated by Django 3.2.7 on 2021-09-07 14:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('github_profile', '0002_remove_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='id',
        ),
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.CharField(default=None, max_length=30),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.CharField(default=None, max_length=30, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_update',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
