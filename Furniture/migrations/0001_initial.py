# Generated by Django 4.2.3 on 2023-08-04 22:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/categories')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FurnitureAd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('rating', models.IntegerField()),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('currency', models.CharField(max_length=3)),
                ('width', models.IntegerField()),
                ('length', models.IntegerField()),
                ('height', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('unit_weight', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/furnitures')),
                ('status', models.CharField(max_length=100)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('ad_duration_to', models.DateField()),
                ('views', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Furniture.category')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PE', 'Pending'), ('AC', 'Accepted'), ('CA', 'Cancelled'), ('DE', 'Delivered')], default='PE', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='UrbanNestUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/users')),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=100)),
                ('province', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('phone_number', models.CharField(max_length=9)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('PE', 'Pending'), ('AC', 'Accepted'), ('CA', 'Cancelled'), ('DE', 'Delivered')], default='PE', max_length=2)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Furniture.urbannestuser')),
                ('items', models.ManyToManyField(to='Furniture.orderitem')),
            ],
        ),
        migrations.AddField(
            model_name='orderitem',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Furniture.urbannestuser'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='furniture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Furniture.furnituread'),
        ),
        migrations.AddField(
            model_name='furnituread',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Furniture.urbannestuser'),
        ),
    ]
