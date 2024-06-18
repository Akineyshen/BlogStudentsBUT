from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile

from django.conf import settings

def createProfile(sender, instance, created, **kwargs):
    """
    Creates a Profile instance for a new User when the User instance is created.

    Args:
        sender (type): The model class that sent the signal.
        instance (User): The instance of the User model that was saved.
        created (bool): A boolean indicating whether a new record was created.
        **kwargs: Additional keyword arguments.

    This function performs the following tasks:
        1. Checks if the User instance was created (not updated).
        2. If a new User was created, retrieves the user instance.
        3. Creates a new Profile instance with the user's details.

    This function is intended to be connected to the `post_save` signal of the User model.

    Example:
        post_save.connect(createProfile, sender=User)
    """
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )



def updateUser(sender, instance, created, **kwargs):
    """
    Updates the User instance associated with a Profile when the Profile is updated.

    Args:
        sender (type): The model class that sent the signal.
        instance (Profile): The instance of the Profile model that was saved.
        created (bool): A boolean indicating whether a new record was created.
        **kwargs: Additional keyword arguments.

    This function performs the following tasks:
        1. Retrieves the Profile instance that was saved.
        2. Retrieves the associated User instance.
        3. If the Profile instance was not newly created (i.e., it was updated):
            a. Updates the User's first name, username, and email to match the Profile.
            b. Saves the updated User instance.

    This function is intended to be connected to the `post_save` signal of the Profile model.

    Example:
        post_save.connect(updateUser, sender=Profile)
    """
    profile = instance
    user = profile.user

    if created==False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    """
    Deletes the User instance associated with a Profile when the Profile is deleted.

    Args:
        sender (type): The model class that sent the signal.
        instance (Profile): The instance of the Profile model that is being deleted.
        **kwargs: Additional keyword arguments.

    This function performs the following tasks:
        1. Tries to retrieve the User instance associated with the Profile.
        2. If the User instance is found, deletes the User instance.
        3. If any exception occurs (e.g., the User instance does not exist), it silently passes without error.

    This function is intended to be connected to the `pre_delete` signal of the Profile model.

    Example:
        pre_delete.connect(deleteUser, sender=Profile)
    """
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)