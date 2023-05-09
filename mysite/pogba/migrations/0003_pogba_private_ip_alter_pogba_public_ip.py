# Generated by Django 4.1.7 on 2023-04-11 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pogba', '0002_rename_body_pogba_public_ip_remove_pogba_answer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pogba',
            name='private_ip',
            field=models.GenericIPAddressField(default='127.0.0.1'),
        ),
        migrations.AlterField(
            model_name='pogba',
            name='public_ip',
            field=models.CharField(max_length=255),
        ),
    ]
