# Generated by Django 4.1.10 on 2023-08-30 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='category_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='post.category'),
            preserve_default=False,
        ),
    ]
