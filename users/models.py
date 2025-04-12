from django.db import models
from django.contrib.auth.models import User
import uuid


class Skill(models.Model):
    """
    A model representing a skill (Faculty).

    Attributes:
        name (str): The name of the faculty. It can be blank or null.
        slug (str): A URL-friendly slug identifier for the faculty.
        created (datetime): The date and time when the faculty was created. Automatically set on creation.
        id (UUID): A unique identifier for the faculty, generated automatically.

    Methods:
        __str__(): Returns the string representation of the skill, which is the skill's name.
    """
    name = models.CharField(max_length=80, blank=True, null=True)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


class Profile(models.Model):
    """
    A model representing a user profile.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the User model. Can be null or blank.
        name (str): The name of the user. Default is 'no_email'.
        email (str): The email of the user. Default is 'no name'.
        username (str): The username of the user. Can be blank or null.
        intro (str): A short introduction for the profile. Can be blank or null.
        bio (TextField): A detailed biography for the profile. Can be blank or null.
        image (ImageField): The profile image. Defaults to 'profile_images/default.jpg'. Can be blank or null.
        skills (ManyToManyField): A many-to-many relationship with the Skill model. Can be blank.
        facebook (str): The Facebook profile link. Can be blank or null.
        instagram (str): The Instagram profile link. Can be blank or null.
        created (datetime): The date and time when the profile was created. Automatically set on creation.
        id (UUID): A unique identifier for the profile, generated automatically.

    Methods:
        __str__(): Returns the string representation of the profile, which is the profile's username.

    Meta:
        ordering (list): Specifies the default ordering of profiles by the 'created' field.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, blank=False, default="no_email")
    email = models.EmailField(max_length=50, blank=False, default='no name')
    username = models.CharField(max_length=50, blank=True, null=True)
    intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='profile_images', default="profile_images/default.jpg")
    skills = models.ManyToManyField(Skill, blank=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['created']


class Message(models.Model):
    """
    A model representing a message sent between profiles.

    Attributes:
        sender (ForeignKey): The profile that sent the message. Can be null or blank. Deletes set to NULL on profile deletion.
        recipient (ForeignKey): The profile that received the message. Can be null or blank. Deletes set to NULL on profile deletion.
        name (str): The name of the sender. Can be null or blank.
        email (str): The email of the sender. Can be null or blank.
        subject (str): The subject of the message. Can be null or blank.
        body (TextField): The body of the message.
        is_read (bool): Indicates if the message has been read. Defaults to False. Can be null.
        created (datetime): The date the message was created. Automatically set on creation.
        id (UUID): A unique identifier for the message, generated automatically.

    Methods:
        __str__(): Returns the string representation of the message, which is the message's subject.

    Meta:
        ordering (list): Specifies the default ordering of messages, first by 'is_read' status and then by 'created' date in descending order.
    """
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']