# Generated by Django 5.0.4 on 2024-05-06 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0011_remove_article_tags_article_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='tag',
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, to='articles.tag'),
        ),
    ]