# Generated by Django 4.1.2 on 2022-11-30 23:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LibraryCatalog', '0012_alter_bookinstance_labelid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='borrower',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='borrowed', to=settings.AUTH_USER_MODEL),
        ),
    ]
