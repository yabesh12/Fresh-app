# Generated by Django 3.2.10 on 2022-07-27 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupBasedPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('discount_selling_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('price_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='group.pricegroup')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_based_product', to='product.product')),
            ],
            options={
                'unique_together': {('price_group', 'product')},
            },
        ),
    ]