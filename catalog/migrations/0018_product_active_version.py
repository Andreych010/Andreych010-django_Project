# Generated by Django 4.2.3 on 2023-08-05 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_alter_version_number_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='active_version',
            field=models.BooleanField(blank=True, null=True, verbose_name='признак текущей версии'),
        ),
    ]