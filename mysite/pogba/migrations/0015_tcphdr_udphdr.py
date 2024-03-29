# Generated by Django 4.1.7 on 2023-05-17 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pogba', '0014_alter_event_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='tcphdr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.PositiveIntegerField()),
                ('cid', models.PositiveIntegerField()),
                ('tcp_sport', models.PositiveIntegerField()),
                ('tcp_dport', models.PositiveIntegerField()),
                ('tcp_seq', models.PositiveSmallIntegerField()),
                ('tcp_ack', models.PositiveSmallIntegerField()),
                ('tcp_flags', models.PositiveSmallIntegerField()),
            ],
            options={
                'db_table': 'tcphdr',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='udphdr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.PositiveIntegerField()),
                ('cid', models.PositiveIntegerField()),
                ('udp_sport', models.PositiveIntegerField()),
                ('udp_dport', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'udphdr',
                'managed': False,
            },
        ),
    ]
