# Generated by Django 3.2.10 on 2022-07-27 09:05

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200, unique=True)),
                ('unit', models.CharField(choices=[('PENDING', 'PENDING'), ('KG', 'KG'), ('GRAM', 'GRAM'), ('DOZEN', 'DOZEN'), ('PACKET', 'PACKET'), ('CASE', 'CASE')], default='PENDING', max_length=150)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=7)),
                ('is_credit_available', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.producttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('sku', models.CharField(max_length=200, unique=True)),
                ('shelf_life', models.PositiveIntegerField()),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('mrp_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('unit', models.CharField(choices=[('PENDING', 'PENDING'), ('KG', 'KG'), ('GRAM', 'GRAM'), ('DOZEN', 'DOZEN'), ('PACKET', 'PACKET'), ('CASE', 'CASE')], default='PENDING', max_length=150)),
                ('weight', models.CharField(max_length=150)),
                ('is_active', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('category', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_category', to='product.category')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('product_type', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_type', to='product.producttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='category',
            name='product_type',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_product_type', to='product.producttype'),
        ),
    ]
