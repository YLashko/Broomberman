# Generated by Django 4.2.2 on 2023-06-08 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='game',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Game',
        ),
    ]
