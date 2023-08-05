# Generated by Django 4.2.3 on 2023-08-05 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Furniture', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/testimonials')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='urbannestuser',
            name='shopping_cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Furniture.shoppingcart'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='buyer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Furniture.urbannestuser'),
        ),
        migrations.AlterField(
            model_name='urbannestuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
