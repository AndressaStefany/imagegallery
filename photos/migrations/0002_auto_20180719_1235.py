# Generated by Django 2.0.7 on 2018-07-19 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='quantity_like',
            new_name='like_count',
        ),
        migrations.RenameField(
            model_name='images',
            old_name='caminho',
            new_name='path',
        ),
    ]
