# Generated by Django 4.1.3 on 2022-11-03 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_alter_post_status'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='post',
            table='questions',
        ),
    ]
