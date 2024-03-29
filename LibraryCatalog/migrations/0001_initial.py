# Generated by Django 4.1.2 on 2022-10-31 21:38

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('date_of_death', models.DateField(blank=True, null=True)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('summary', models.TextField(max_length=1000)),
                ('isbn', models.CharField(max_length=13, unique=True, verbose_name='ISBN')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LibraryCatalog.author')),
            ],
        ),
        migrations.CreateModel(
            name='BookGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_name', models.CharField(help_text='Enter a book genre', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='BookInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('o', 'ON LOAN'), ('h', 'ON HOLD'), ('a', 'AVAILABLE'), ('u', 'UNAVAILABLE')], default='u', help_text='Current Book Status', max_length=1)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='LibraryCatalog.book')),
            ],
            options={
                'ordering': ['due_date'],
            },
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(to='LibraryCatalog.bookgenre'),
        ),
    ]
