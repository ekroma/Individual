# Generated by Django 4.1.3 on 2022-11-03 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='image',
            field=models.ImageField(blank=True, upload_to='post_images'),
        ),
    ]
