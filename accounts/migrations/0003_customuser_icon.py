# Generated by Django 5.1.1 on 2024-10-17 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='icon',
            field=models.ImageField(default='F:\\Llama\\django-chat-app\\static\x07dmin\\img\\icon\\kkrn_icon_user_1-768x768.png', upload_to='images/'),
        ),
    ]
