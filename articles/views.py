import articles
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Tag, Review
from .forms import ArticleForm, ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import paginator
from .utils import paginateArticles, searchArticles
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.conf import settings
import os
from PIL import Image
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseServerError
from django.core.paginator import Paginator


def articles_main(request):
    """
    Handles the main view for displaying articles with pagination functionality.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object with the rendered 'articles/articles_main.html' template.

    This view function performs the following tasks:
        1. Paginates the retrieved articles using the paginateArticles function, displaying 12 articles per page.
        2. Prepares the context with the articles, search query, and custom pagination range.
        3. Renders the 'articles/articles_main.html' template with the context.  
    """
    articles, search_query = searchArticles(request)
    custom_range, articles = paginateArticles(request, articles, 12)
    context = {'articles': articles, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'articles/articles_main.html', context)


def articles(request):
    """
    Handles the main view for displaying articles with search and pagination functionality.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object with the rendered 'articles/articles_main.html' template.

    This view function performs the following tasks:
        1. Retrieves articles based on a search query using the searchArticles function.
        2. Paginates the retrieved articles using the paginateArticles function, displaying 12 articles per page.
        3. Prepares the context with the articles, search query, and custom pagination range.
        4. Renders the 'articles/articles_main.html' template with the context.
    """
    articles, search_query = searchArticles(request)
    custom_range, articles = paginateArticles(request, articles, 6)
    context = {'articles': articles, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'articles/articles.html', context)


def article(request, article_slug):
    """
    Handles the view for displaying a single article, including handling private articles and comments.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        article_slug (str): The slug identifier for the article to be displayed.

    Returns:
        HttpResponse: The HTTP response object with the rendered article template or password form.

    This view function performs the following tasks:
        1. Retrieves the article based on the provided slug or returns a 404 if not found.
        2. Fetches all tags associated with the article.
        3. Initializes a blank review form.
        4. If the article is private and the session does not have authorization, it checks the password:
            a. If the password is correct, sets the session authorization and redirects to the article.
            b. If the password is incorrect or not provided, renders the password form.
        5. If a comment is posted, validates the form and saves the review, associating it with the article and the user.
        6. Renders the article with its details, tags, and the review form.

    The context for rendering the templates includes:
        - article: The article object.
        - form: The review form.
        - tags: The tags associated with the article.
    """
    article = get_object_or_404(Article, slug=article_slug)
    tags = article.tags.all()
    form = ReviewForm()

    if article.is_private and not request.session.get(article_slug + '_auth'):
        if request.method == 'POST' and 'password' in request.POST:
            if article.check_password(request.POST['password']):
                request.session[article_slug + '_auth'] = True
                messages.success(request, 'Password correct, you can now view the article.')
                return redirect('article', article_slug=article_slug)
            else:
                messages.error(request, 'Incorrect password')
                return render(request, 'articles/password_form.html', {'article': article})
        return render(request, 'articles/password_form.html', {'article': article})

    if request.method == 'POST' and 'comment' in request.POST:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.article = article
            review.owner = request.user.profile
            review.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('article', article_slug=article.slug)

    return render(request, 'articles/single_article.html', {'article': article, 'form': form, 'tags': tags})


@login_required(login_url="login")
def createArticle(request):
    """
    Handles the creation of a new article by the logged-in user.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object with the rendered article form template or a redirect to the user's account page.

    This view function performs the following tasks:
        1. Initializes an empty ArticleForm for GET requests.
        2. Processes POST requests with form data and files:
            a. If the form is valid:
                i. Saves the article instance without committing to set the owner.
                ii. Sets a password for private articles.
                iii. Saves the article instance.
                iv. Adds tags to the article.
                v. Redirects to the user's account page.
            b. If the form is invalid, it continues to render the form with errors.
        3. Renders the article form template with the form context.

    The context for rendering the template includes:
        - form: The ArticleForm instance for creating a new article.
    """
    form = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.owner = request.user.profile
            if form.cleaned_data['is_private']:
                article.set_password(form.cleaned_data['password'])
            article.save()
            article.tags.add(form.cleaned_data['tag'])
            return redirect('account')
    context = {'form': form}
    return render(request, "articles/article_form.html", context)


@login_required(login_url="login")
def updateArticle(request, pk):
    """
    Handles the updating of an existing article by the logged-in user.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        pk (str): The primary key of the article to be updated.

    Returns:
        HttpResponse: The HTTP response object with the rendered article form template or a redirect to the user's account page.

    This view function performs the following tasks:
        1. Retrieves the profile of the logged-in user.
        2. Retrieves the article instance associated with the user and the provided primary key.
        3. Initializes the ArticleForm with the article instance for GET requests.
        4. Processes POST requests with form data and files:
            a. If the form is valid:
                i. Saves the updated article instance.
                ii. Clears existing tags and adds the new tags from the form.
                iii. Redirects to the user's account page.
            b. If the form is invalid, it continues to render the form with errors.
        5. Renders the article form template with the form and article context.

    The context for rendering the template includes:
        - form: The ArticleForm instance for updating the article.
        - article: The article instance being updated.
    """
    profile = request.user.profile
    article = profile.article_set.get(id=pk)
    form = ArticleForm(instance=article)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save()
            article.tags.clear()
            article.tags.add(form.cleaned_data['tag'])

            return redirect('account')

    context = {'form': form, 'article': article, }
    return render(request, "articles/article_form.html", context)


@login_required(login_url="login")
def deleteArticle(request, pk):
    """
    Handles the deletion of an existing article by the logged-in user.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        pk (str): The primary key of the article to be deleted.

    Returns:
        HttpResponse: The HTTP response object with the rendered delete confirmation template or a redirect to the articles list page.

    This view function performs the following tasks:
        1. Retrieves the profile of the logged-in user.
        2. Retrieves the article instance associated with the user and the provided primary key.
        3. If the request method is POST, deletes the article and redirects to the articles list page.
        4. If the request method is GET, renders the delete confirmation template.

    The context for rendering the template includes:
        - object: The article instance being deleted.
    """
    profile = request.user.profile
    article = profile.article_set.get(id=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('articles')
    context = {'object': article}
    return render(request, 'delete_template.html', context)


def articles_by_tag(request, tag_slug):
    """
    Handles the view for displaying articles filtered by a specific tag.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        tag_slug (str): The slug identifier for the tag to filter articles by.

    Returns:
        HttpResponse: The HTTP response object with the rendered articles template.

    This view function performs the following tasks:
        1. Retrieves the tag instance based on the provided slug or returns a 404 if not found.
        2. Filters articles that are associated with the retrieved tag.
        3. Prepares the context with the filtered articles.
        4. Renders the articles template with the context.

    The context for rendering the template includes:
        - articles: The list of articles associated with the specified tag.
    """
    tag = get_object_or_404(Tag, slug=tag_slug)
    articles =Article.objects.filter(tags__in=[tag])
    context = {
        "articles": articles
    }

    return render(request, "articles/articles.html", context)


def edit_review(request, review_id):
    """
    Handles the view for editing an existing review.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        review_id (str): The ID of the review to be edited.

    Returns:
        HttpResponse: The HTTP response object with the rendered edit review template or a redirect to the associated article.

    This view function performs the following tasks:
        1. Retrieves the review instance based on the provided review ID or returns a 404 if not found.
        2. Initializes the ReviewForm with the review instance for GET requests.
        3. Processes POST requests with form data:
            a. If the form is valid, saves the updated review and redirects to the associated article.
            b. If the form is invalid, it continues to render the form with errors.
        4. Renders the edit review template with the form and review context.

    The context for rendering the template includes:
        - form: The ReviewForm instance for editing the review.
        - review: The review instance being edited.
    """
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('article', article_slug=review.article.slug)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'articles/edit_comment.html', {'form': form, 'review': review})


def delete_review(request, review_id):
    """
    Handles the deletion of an existing review.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        review_id (str): The ID of the review to be deleted.

    Returns:
        HttpResponse: The HTTP response object with the rendered delete confirmation template or a redirect to the associated article.

    This view function performs the following tasks:
        1. Retrieves the review instance based on the provided review ID or returns a 404 if not found.
        2. If the request method is POST and the delete confirmation is present in the request, deletes the review and redirects to the associated article.
        3. If the request method is GET, renders the delete confirmation template.

    The context for rendering the template includes:
        - review: The review instance being deleted.
    """
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        if 'confirm_delete' in request.POST:
            review.delete()
            return redirect('article', article_slug=review.article.slug)
    return render(request, 'articles/delete_comment.html', {'review': review})


def get_image_size(image_path):
    """
    Retrieves the dimensions of an image.

    Args:
        image_path (str): The path to the image file.

    Returns:
        tuple: A tuple containing the width and height of the image in pixels.

    This function performs the following tasks:
        1. Opens the image file located at the specified path.
        2. Retrieves the dimensions (width and height) of the image.
        3. Returns the dimensions as a tuple (width, height).
    """
    with Image.open(image_path) as img:
        return img.size


def generate_pdf(request, article_slug):
    """
    Generates a PDF for a specific article and serves it as a downloadable file.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        article_slug (str): The slug identifier for the article to generate the PDF for.

    Returns:
        HttpResponse: The HTTP response object containing the generated PDF.

    This view function performs the following tasks:
        1. Retrieves the article based on the provided slug or returns a 404 if not found.
        2. Sets up the HTTP response for a PDF file with the appropriate content type and headers.
        3. Determines the image path if the article has an associated image.
        4. Renders the HTML content for the PDF using a template.
        5. Uses xhtml2pdf to generate the PDF from the HTML content.
        6. If there are errors during PDF generation, returns an error response.
        7. Returns the generated PDF as an HTTP response.

    The context for rendering the PDF template includes:
        - article: The article instance for which the PDF is being generated.
        - image_path: The file path of the article's associated image, if any.
    """
    article = get_object_or_404(Article, slug=article_slug)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{article.slug}.pdf"'

    image_path = os.path.join(settings.MEDIA_ROOT, article.image.name) if article.image else None

    html_content = render_to_string('articles/pdf_template.html', {
        'article': article,
        'image_path': image_path,
    })

    pisa_status = pisa.CreatePDF(html_content, dest=response, link_callback=link_callback)

    if pisa_status.err:
        return HttpResponse(f'We had some errors with code {pisa_status.err}')

    return response

def link_callback(uri, rel):
    """
    Converts URIs in the PDF generation HTML to the appropriate absolute file system paths.

    Args:
        uri (str): The URI that needs to be converted to a file path.
        rel (str): A relative path, typically unused in this context.

    Returns:
        str: The absolute file system path corresponding to the given URI.

    This function performs the following tasks:
        1. Determines the base URL and root directory for static and media files from the Django settings.
        2. Checks if the URI starts with the media or static URL, and converts it to the corresponding file system path.
        3. If the URI does not match media or static URLs, returns the URI as is (for absolute URLs).
        4. Raises an exception if the converted path does not correspond to an existing file.

    Raises:
        Exception: If the URI does not start with the media or static URL, or if the file does not exist at the converted path.
    """
    sUrl = settings.STATIC_URL  # Typically /static/
    sRoot = settings.STATIC_ROOT  # Typically /var/www/example.com/static/
    mUrl = settings.MEDIA_URL  # Typically /media/
    mRoot = settings.MEDIA_ROOT  # Typically /var/www/example.com/media/

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (i.e. http://some.tld/foo.png)

    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with {} or {}'.format(sUrl, mUrl)
        )
    return path