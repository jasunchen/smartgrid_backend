# Generated by Django 3.1.13 on 2021-12-12 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_ag_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ag_user_asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, max_length=254)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.ag_user')),
            ],
        ),
        migrations.CreateModel(
            name='ag_asset_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('interval', models.IntegerField()),
                ('consumed_energy', models.FloatField()),
                ('produced_energy', models.FloatField()),
                ('asset_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.ag_user_asset')),
            ],
        ),
    ]
