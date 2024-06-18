from .models import Article, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateArticles(request, articles, results):
    """
    Paginates a queryset of articles and provides a custom range for pagination controls.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        articles (QuerySet): The queryset of articles to be paginated.
        results (int): The number of articles to display per page.

    Returns:
        tuple: A tuple containing:
            - custom_range (range): A range of page numbers for pagination controls.
            - articles (Page): A Page object containing the articles for the current page.

    This function performs the following tasks:
        1. Retrieves the current page number from the request's GET parameters.
        2. Initializes a Paginator object with the articles queryset and the specified number of results per page.
        3. Tries to get the articles for the specified page:
            a. If the page number is not an integer, defaults to the first page.
            b. If the page number is out of range, defaults to the last page.
        4. Calculates the range of page numbers to display in pagination controls:
            a. Ensures the left index is not less than 1.
            b. Ensures the right index does not exceed the total number of pages plus one.
        5. Returns the custom range of page numbers and the Page object for the current page.

    Example:
        >>> custom_range, articles = paginateArticles(request, articles, 10)
    """
    page = request.GET.get('page')
    paginator = Paginator(articles, results)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        articles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        articles = paginator.page(page)

    leftIndex = (int(page)-4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, articles

def searchArticles(request):
    """
    Searches for articles based on a search query from the request.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        tuple: A tuple containing:
            - articles (QuerySet): A queryset of articles matching the search query.
            - search_query (str): The search query string used for filtering articles.

    This function performs the following tasks:
        1. Initializes an empty search query string.
        2. Checks if a 'search_query' parameter is present in the GET request:
            a. If present, sets the search query to the value of this parameter.
        3. Filters tags based on the search query using a case-insensitive containment lookup.
        4. Filters articles based on the search query and associated tags:
            a. Matches articles where the title contains the search query.
            b. Matches articles where the description contains the search query.
            c. Matches articles where the owner's name contains the search query.
            d. Matches articles that have tags matching the search query.
        5. Ensures that the resulting article queryset is distinct to avoid duplicate results.
        6. Returns the filtered articles queryset and the search query string.

    Example:
        >>> articles, search_query = searchArticles(request)
    """

    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    articles = Article.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )
    return articles, search_query