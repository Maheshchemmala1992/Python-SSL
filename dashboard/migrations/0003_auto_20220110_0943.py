# Generated by Django 2.2.6 on 2022-01-10 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20220107_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='media/issue'),
        ),
        migrations.AddField(
            model_name='staffuser',
            name='profile_pic',
            field=models.ImageField(default='static/img/undraw_profile.svg', upload_to='media/profile'),
        ),
        migrations.AddField(
            model_name='task',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='media/task'),
        ),
    ]
