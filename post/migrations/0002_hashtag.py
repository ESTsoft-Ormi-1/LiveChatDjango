# Generated by Django 4.1.10 on 2023-08-21 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('writer', models.CharField(max_length=30)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
        ),
    ]
