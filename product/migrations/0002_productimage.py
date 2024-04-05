# Generated by Django 5.0.3 on 2024-04-03 21:22

import django.db.models.deletion
import product.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('alternative_text', models.CharField(max_length=100)),
                ('url', models.ImageField(upload_to=None)),
                ('order', product.fields.OrderField(blank=True)),
                ('product_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to='product.productline')),
            ],
        ),
    ]
