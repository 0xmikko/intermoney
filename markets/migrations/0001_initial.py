# Generated by Django 2.2 on 2019-04-07 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tickers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, unique=True)),
                ('smart_contract_address', models.CharField(default='0x0', max_length=42)),
                ('base_currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='base_market', to='tickers.Ticker')),
                ('quote_currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quote_market', to='tickers.Ticker')),
            ],
        ),
    ]
