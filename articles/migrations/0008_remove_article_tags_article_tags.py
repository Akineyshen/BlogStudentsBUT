# Generated by Django 5.0.4 on 2024-05-05 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_remove_article_tags_article_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='tags',
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, to='articles.tag'),
        ),
    ]