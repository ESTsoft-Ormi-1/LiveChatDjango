# Generated by Django 4.1.10 on 2023-09-01 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]
