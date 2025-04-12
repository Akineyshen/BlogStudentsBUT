from django.test import TestCase, Client
from django.urls import reverse
from .models import Article, Tag, Review
from users.models import Profile
from django.contrib.auth.models import User

class ArticlesViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.profile, created = Profile.objects.get_or_create(user=cls.user)
        cls.tag = Tag.objects.create(name="Django")
        cls.article = Article.objects.create(
            owner=cls.profile,
            title="Test Article",
            slug="test-article",
            description="A description of the test article",
            is_private=False
        )
        cls.article.tags.add(cls.tag)
        cls.review = Review.objects.create(
            owner=cls.profile,
            article=cls.article,
            body="Great article!"
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_articles_main_view(self):
        response = self.client.get(reverse('articles_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/articles_main.html')

    def test_articles_view(self):
        response = self.client.get(reverse('articles'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/articles.html')

    def test_article_view(self):
        response = self.client.get(reverse('article', args=[self.article.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/single_article.html')

    def test_create_article_view(self):
        response = self.client.get(reverse('create_article'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article_form.html')

    def test_update_article_view(self):
        response = self.client.get(reverse('update_article', args=[self.article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article_form.html')

    def test_delete_article_view(self):
        response = self.client.get(reverse('delete_article', args=[self.article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_template.html')

    def test_articles_by_tag_view(self):
        response = self.client.get(reverse('tag', args=[self.tag.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/articles.html')

    def test_edit_review_view(self):
        response = self.client.get(reverse('edit_comment', args=[self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/edit_comment.html')

    def test_delete_review_view(self):
        response = self.client.get(reverse('delete_comment', args=[self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/delete_comment.html')


class GeneratePDFTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.profile, created = Profile.objects.get_or_create(user=cls.user)
        cls.article = Article.objects.create(
            owner=cls.profile,
            title="Test Article",
            slug="test-article",
            description="A description of the test article",
            is_private=False
        )

    def setUp(self):
        self.client = Client()

    def test_generate_pdf_view(self):
        response = self.client.get(reverse('generate_pdf', args=[self.article.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
