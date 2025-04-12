from .models import Profile, Skill
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

def paginateProfiles(request, profiles, results):
    """
    Paginates a queryset of profiles and provides a custom range for pagination controls.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        profiles (QuerySet): The queryset of profiles to be paginated.
        results (int): The number of profiles to display per page.

    Returns:
        tuple: A tuple containing:
            - custom_range (range): A range of page numbers for pagination controls.
            - profiles (Page): A Page object containing the profiles for the current page.

    This function performs the following tasks:
        1. Retrieves the current page number from the request's GET parameters.
        2. Initializes a Paginator object with the profiles queryset and the specified number of results per page.
        3. Tries to get the profiles for the specified page:
            a. If the page number is not an integer, defaults to the first page.
            b. If the page number is out of range, defaults to the last page.
        4. Calculates the range of page numbers to display in pagination controls:
            a. Ensures the left index is not less than 1.
            b. Ensures the right index does not exceed the total number of pages plus one.
        5. Returns the custom range of page numbers and the Page object for the current page.

    Example:
        >>> custom_range, profiles = paginateProfiles(request, profiles, 6)
    """
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5 )

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles


def searchProfiles(request):
    """
    Searches for profiles based on a search query from the request.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        tuple: A tuple containing:
            - profiles (QuerySet): A queryset of profiles matching the search query.
            - search_query (str): The search query string used for filtering profiles.

    This function performs the following tasks:
        1. Initializes an empty search query string.
        2. Checks if a 'search_query' parameter is present in the GET request:
            a. If present, sets the search query to the value of this parameter.
        3. Filters skills based on the search query using a case-insensitive containment lookup.
        4. Filters profiles based on the search query and associated skills:
            a. Matches profiles where the name contains the search query.
            b. Matches profiles where the intro contains the search query.
            c. Matches profiles that have skills matching the search query.
        5. Ensures that the resulting profile queryset is distinct to avoid duplicate results.
        6. Returns the filtered profiles queryset and the search query string.

    Example:
        >>> profiles, search_query = searchProfiles(request)
    """
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(intro__icontains=search_query) |
        Q(skills__in=skills)
    )
    return profiles, search_query