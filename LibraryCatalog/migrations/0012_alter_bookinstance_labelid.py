# Generated by Django 4.1.2 on 2022-11-17 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryCatalog', '0011_rename_labelid_bookinstance_labelid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='labelId',
            field=models.CharField(max_length=13, unique=True),
        ),
    ]
