# Generated by Django 4.1.7 on 2023-03-25 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(default='default_pic.png', upload_to='book_pictures/user_pictures'),
        ),
    ]
