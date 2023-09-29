# Generated by Django 4.2.5 on 2023-09-28 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopper',
            name='username',
        ),
        migrations.AlterField(
            model_name='shopper',
            name='email',
            field=models.EmailField(max_length=240, unique=True),
        ),
    ]
