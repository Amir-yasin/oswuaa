# Generated by Django 5.0.6 on 2024-05-19 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osu_app', '0002_category_customuser_gender_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.ImageField(default='default.jpeg', upload_to='profile_images/'),
        ),
    ]
