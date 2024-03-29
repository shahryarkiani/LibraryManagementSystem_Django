# Generated by Django 4.1.2 on 2022-12-28 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryCatalog', '0015_bookinstance_librarycata_labelid_cb08bd_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='hold_status',
            field=models.CharField(blank=True, choices=[('n', 'NO HOLDS'), ('r', 'HOLD REQUESTED'), ('h', 'ON HOLD - READY FOR PICKUP')], default='n', max_length=1),
        ),
    ]
