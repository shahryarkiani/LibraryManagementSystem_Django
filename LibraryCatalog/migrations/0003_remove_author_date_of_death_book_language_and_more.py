# Generated by Django 4.1.2 on 2022-10-31 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryCatalog', '0002_alter_book_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='date_of_death',
        ),
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.CharField(blank=True, choices=[('e', 'ENGLISH'), ('s', 'SPANISH'), ('o', 'OTHER')], default='u', help_text='Language the book is written in', max_length=1),
        ),
        migrations.AlterField(
            model_name='author',
            name='date_of_birth',
            field=models.DateField(blank=True, help_text="Enter the Author's date of birth", null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='first_name',
            field=models.CharField(help_text='Enter the First Name of the Author', max_length=100),
        ),
        migrations.AlterField(
            model_name='author',
            name='last_name',
            field=models.CharField(help_text='Enter the Last Name of the Author', max_length=100),
        ),
    ]
