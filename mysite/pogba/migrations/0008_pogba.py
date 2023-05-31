# Generated by Django 4.1.7 on 2023-05-17 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pogba', '0007_delete_pogba'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pogba',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_ip', models.CharField(max_length=255)),
                ('private_ip', models.GenericIPAddressField(default='127.0.0.1')),
            ],
        ),
    ]
