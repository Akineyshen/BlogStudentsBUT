# Generated by Django 5.0.4 on 2024-05-02 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_article_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, default='article_img/default.jpg', null=True, upload_to='article_img'),
        ),
    ]
