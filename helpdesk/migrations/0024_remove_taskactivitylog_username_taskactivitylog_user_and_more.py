# Generated by Django 5.2 on 2025-05-15 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0023_remove_taskactivitylog_user_taskactivitylog_username_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskactivitylog',
            name='username',
        ),
        migrations.AddField(
            model_name='taskactivitylog',
            name='user',
            field=models.CharField(default=1, verbose_name='Nome do Usuário'),
        ),
        migrations.AlterField(
            model_name='ticketactivitylog',
            name='ticket',
            field=models.CharField(default=1, verbose_name='Ticket'),
        ),
        migrations.AlterField(
            model_name='ticketactivitylog',
            name='user',
            field=models.CharField(default=1, verbose_name='Nome do Usuário'),
        ),
    ]
