# Generated by Django 5.0.4 on 2024-04-24 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_tag_article_total_votes_article_votes_ratio_comment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, default='article_img/default.png', null=True, upload_to='article_img'),
        ),
    ]