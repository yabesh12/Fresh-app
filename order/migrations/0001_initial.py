# Generated by Django 3.2.10 on 2022-07-27 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
        ('sales_executive', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending', max_length=150)),
                ('bill_date', models.DateField(blank=True, null=True)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('is_paid', models.BooleanField(default=False)),
                ('paid_date', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('out_standing_credit', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('billed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='sales_executive.salesexecutive')),
                ('billed_to', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='shop.shop')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=7, max_length=100)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
