# Generated by Django 4.1.2 on 2022-11-01 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryCatalog', '0004_bookinstance_isbn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='isbn',
            field=models.CharField(max_length=13, verbose_name='ISBN'),
        ),
    ]
