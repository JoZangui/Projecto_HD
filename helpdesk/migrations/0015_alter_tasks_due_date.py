# Generated by Django 5.2 on 2025-05-02 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0014_alter_tasks_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
