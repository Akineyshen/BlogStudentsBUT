from django.db import models
import uuid
from users.models import Profile
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password, check_password


class Tag(models.Model):
    """
    A model representing a tag(Faculty) for articles.

    Attributes:
        name (str): The name of the Faculty.
        slug (str): A URL-friendly, unique identifier generated from the name.
        created (datetime): The date and time when the faculty was created.
        id (UUID): A unique identifier for the faculty, generated automatically.

    Methods:
        save(*args, **kwargs): Overrides the save method to ensure the slug is generated from the name.
        __str__(): Returns the name of the faculty as its string representation.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    A model representing an article.

    Attributes:
        owner (ForeignKey): The profile of the user who owns the article. Can be null or blank.
        title (str): The title of the article.
        slug (str): A URL-friendly identifier for the article.
        image (ImageField): An optional image associated with the article. Defaults to 'article_img/default.jpg'.
        description (TextField): An optional description of the article.
        tags (ManyToManyField): A set of faculty associated with the article.
        total_votes (int): The total number of comments received by the article. Default value is 0.
        votes_ratio (int): The ratio of votes the article has received. Defaults to 0. (Not used on the site!)
        demo_link (str): An optional demo link related to the article. (Not used on the site!)
        source_link (str): An optional source link related to the article.
        created (datetime): The date and time when the article was created.
        id (UUID): A unique identifier for the article, generated automatically.
        is_private (bool): A flag indicating if the article is private. Defaults to False.
        password (str): An optional password for the article. Can be null or blank.

    Methods:
        set_password(raw_password): Sets the password for the article using Django's password hashing.
        check_password(raw_password): Checks if a given raw password matches the article's password.
        save(*args, **kwargs): Overrides the save method to ensure passwords are hashed before saving.
        __str__(): Returns the title of the article as its string representation.
        review_count(): Returns the count of reviews associated with the article.
        reviewers(): Returns a queryset of IDs of the reviewers who have reviewed the article.
    """
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    image = models.ImageField(null=True, blank=True, default='article_img/default.jpg', upload_to='article_img')
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    total_votes = models.IntegerField(default=0, null=True,blank=True)
    votes_ratio = models.IntegerField(default=0, null=True, blank=True)
    demo_link = models.CharField(max_length=500, null=True, blank=True)
    source_link = models.CharField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    is_private = models.BooleanField(default=False)
    password = models.CharField(max_length=255, blank=True, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def review_count(self):
        return self.review_set.count()

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset


class Review(models.Model):
    """
    A model representing a comment for an article.

    Attributes:
        owner (ForeignKey): The profile of the user who wrote the comment. Can be null.
        article (ForeignKey): The article that the comment is associated with.
        body (TextField): The content of the comment. Can be null or blank.
        created (datetime): The date and time when the comment was created.
        id (UUID): A unique identifier for the comment, generated automatically.

    Methods:
        __str__(): Returns a string representation of the comment, including the owner's profile and the associated article.
    """
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f"{self.owner}'s review on {self.article}"