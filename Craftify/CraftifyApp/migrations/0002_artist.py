# Generated by Django 4.2.2 on 2023-07-07 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CraftifyApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.IntegerField()),
                ('skills', models.CharField(max_length=200)),
                ('image1', models.ImageField(upload_to='image')),
                ('image2', models.ImageField(upload_to='image')),
                ('image3', models.ImageField(upload_to='image')),
                ('address', models.CharField(max_length=300)),
                ('status', models.CharField(default='Not Paid', max_length=100)),
            ],
        ),
    ]
