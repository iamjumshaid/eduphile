# Generated by Django 2.2 on 2021-01-16 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cls_name', models.TextField()),
                ('total_std', models.IntegerField()),
                ('total_attempts', models.IntegerField()),
            ],
        ),
    ]
