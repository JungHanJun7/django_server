# Generated by Django 4.1.7 on 2023-04-02 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pogba", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="pogba", old_name="body", new_name="public_ip",
        ),
        migrations.RemoveField(model_name="pogba", name="answer",),
        migrations.RemoveField(model_name="pogba", name="title",),
    ]
