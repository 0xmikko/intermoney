# Generated by Django 2.2 on 2019-04-06 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickers', '0001_initial'),
        ('markets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='base_currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='base_market', to='tickers.Ticker'),
        ),
        migrations.AddField(
            model_name='market',
            name='quote_currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quote_market', to='tickers.Ticker'),
        ),
    ]
