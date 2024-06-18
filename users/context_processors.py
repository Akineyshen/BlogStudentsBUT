from django.contrib.auth.decorators import login_required

def unread_messages_count(request):
    """
    Retrieves the count of unread messages for the authenticated user's profile.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        dict: A dictionary with the key 'unreadCount' and the count of unread messages as its value.
              If the user is not authenticated, returns an empty dictionary.

    This function performs the following tasks:
        1. Checks if the user is authenticated.
        2. If authenticated, retrieves the user's profile.
        3. Counts the number of unread messages associated with the profile.
        4. Returns a dictionary containing the count of unread messages.
        5. If the user is not authenticated, returns an empty dictionary.

    Example:
        >>> unread_messages_count(request)
        {'unreadCount': 5}
    """
    if request.user.is_authenticated:
        profile = request.user.profile
        unread_count = profile.messages.filter(is_read=False).count()
        return {'unreadCount': unread_count}
    return {}