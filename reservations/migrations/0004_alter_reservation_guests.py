# Generated by Django 4.2.16 on 2024-09-23 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0003_table_description_alter_reservation_table_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="guests",
            field=models.IntegerField(max_length=10),
        ),
    ]
