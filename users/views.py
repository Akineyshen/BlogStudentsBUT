from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, Skill, Message
from django.dispatch.dispatcher import receiver
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import conf
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import paginateProfiles, searchProfiles


def loginUser(request):
    """
    Handles the user login process.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object with the rendered login page or a redirect to the user's profile or account page.

    This view function performs the following tasks:
        1. Checks if the user is already authenticated:
            a. If authenticated, redirects to the 'profile' page.
        2. Handles POST requests to log in the user:
            a. Retrieves the username and password from the POST data.
            b. Tries to get the user with the provided username:
                i. If the user does not exist, adds an error message.
            c. Authenticates the user with the provided credentials:
                i. If the authentication is successful, logs in the user and redirects to the 'next' URL if provided, otherwise to the 'account' page.
                ii. If authentication fails, adds an error message.
        3. Renders the login page template for GET requests or if login fails.

    The context for rendering the template includes:
        - page: The name of the page, used for template rendering logic.
    """
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, 'No users')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        else:
            messages.error(request, 'No invalid username or password')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    """
    Handles the user logout process.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object that redirects the user to the login page.

    This view function performs the following tasks:
        1. Logs out the user by calling Django's `logout` function.
        2. Adds an informational message indicating the user has been logged out.
        3. Redirects the user to the 'login' page.

    Example:
        >>> logoutUser(request)
    """
    logout(request)
    messages.info(request, 'Logged out')
    return redirect('login')


def registerUser(request):
    """
    Handles the user registration process.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object with the rendered registration page or a redirect to the edit account page.

    This view function performs the following tasks:
        1. Sets the page context to 'register'.
        2. Initializes an empty CustomUserCreationForm for GET requests.
        3. Processes POST requests to register a new user:
            a. Populates the CustomUserCreationForm with POST data.
            b. If the form is valid:
                i. Saves the user instance with a lowercase username.
                ii. Displays a success message.
                iii. Logs in the newly registered user.
                iv. Redirects to the 'edit-account' page.
            c. If the form is invalid, displays an error message.
        4. Renders the registration page template with the form context.

    The context for rendering the template includes:
        - page: The name of the page, used for template rendering logic.
        - form: The CustomUserCreationForm instance for user registration.
    """
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'Account created!')

            login(request, user)
            return redirect('edit-account')

        else:
            messages.success(request, 'Something went')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    """
    Handles the view for displaying a list of user profiles with search and pagination functionality.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object with the rendered profiles template.

    This view function performs the following tasks:
        1. Retrieves profiles based on a search query using the searchProfiles function.
        2. Paginates the retrieved profiles using the paginateProfiles function, displaying 6 profiles per page.
        3. Prepares the context with the profiles, search query, and custom pagination range.
        4. Renders the profiles template with the context.

    The context for rendering the template includes:
        - profiles: The paginated list of profiles matching the search query.
        - search_query: The search query string used for filtering profiles.
        - custom_range: The range of page numbers for pagination controls.

    Example:
        >>> profiles(request)
    """
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 6)
    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)



def userProfile(request, username):
    """
    Handles the view for displaying a user's profile, including their main and extra skills.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        username (str): The username of the profile to be displayed.

    Returns:
        HttpResponse: The HTTP response object with the rendered user profile template.

    This view function performs the following tasks:
        1. Retrieves the profile associated with the provided username.
        2. Retrieves the main skills (first 10) and extra skills (all skills starting from the 3rd) of the profile.
        3. Prepares the context with the profile, main skills, and extra skills.
        4. Renders the user profile template with the context.

    The context for rendering the template includes:
        - profile: The Profile instance of the user.
        - main_skills: A list of the first 10 skills of the user.
        - extra_skills: A list of the user's skills starting from the 3rd skill.

    Example:
        >>> userProfile(request, 'john_doe')
    """
    profile = Profile.objects.get(username=username)

    main_skills = profile.skills.all()[:10]
    extra_skills = profile.skills.all()[2:]

    context = {'profile': profile, 'main_skills': main_skills,
               "extra_skills": extra_skills,}
    return render(request, 'users/user_profile.html', context)


def profiles_by_skill(request, skill_slug):
    """
    Handles the view for displaying profiles filtered by a specific faculty.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        skill_slug (str): The slug identifier for the faculty to filter profiles by.

    Returns:
        HttpResponse: The HTTP response object with the rendered profiles template.

    This view function performs the following tasks:
        1. Retrieves the faculty instance based on the provided slug or returns a 404 if not found.
        2. Filters profiles that have the specified faculty.
        3. Prepares the context with the filtered profiles.
        4. Renders the profiles template with the context.

    The context for rendering the template includes:
        - profiles: The list of profiles that have the specified skill.

    Example:
        >>> profiles_by_skill(request, 'Computer Sience')
    """
    skill = get_object_or_404(Skill, slug=skill_slug)
    profiles = Profile.objects.filter(skills=skill)
    context = {'profiles': profiles}
    return render(request, "users/profiles.html", context)


@login_required(login_url='login')
def userAccount(request):
    """
    Handles the view for displaying the logged-in user's account details.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object with the rendered user account template.

    This view function performs the following tasks:
        1. Retrieves the profile of the logged-in user.
        2. Retrieves all skills associated with the user's profile.
        3. Retrieves all articles associated with the user's profile.
        4. Prepares the context with the profile, skills, and articles.
        5. Renders the user account template with the context.

    The context for rendering the template includes:
        - profile: The Profile instance of the logged-in user.
        - skills: A queryset of skills associated with the user's profile.
        - articles: A queryset of articles associated with the user's profile.

    Example:
        >>> userAccount(request)
    """
    profile = request.user.profile

    skills = profile.skills.all()
    articles = profile.article_set.all()

    context = {'profile': profile, 'skills': skills, 'articles': articles}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    """
    Handles the view for editing the logged-in user's account details.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object with the rendered profile form template or a redirect to the user's account page.

    This view function performs the following tasks:
        1. Retrieves the profile of the logged-in user.
        2. Initializes the ProfileForm with the user's profile instance for GET requests.
        3. Processes POST requests to update the user's profile:
            a. Populates the ProfileForm with POST data and files.
            b. If the form is valid, saves the updated profile and redirects to the 'account' page.
        4. Prepares the context with the form.
        5. Renders the profile form template with the context.

    The context for rendering the template includes:
        - form: The ProfileForm instance for editing the user's profile.

    Example:
        >>> editAccount(request)
    """
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    """
    Only for Admin
    """
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.cleaned_data['skill']
            profile.skills.add(skill)
            messages.success(request, 'Faculty successfully added')
            return redirect('account')

    skills = Skill.objects.all()
    context = {'form': form, 'skills': skills}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, skill_slug):
    """
    Handles the view for updating an existing faculty in the logged-in user's profile.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        skill_slug (str): The slug identifier for the faculty to be updated.

    Returns:
        HttpResponse: The HTTP response object with the rendered faculty form template or a redirect to the user's account page.

    This view function performs the following tasks:
        1. Retrieves the profile of the logged-in user.
        2. Retrieves the current faculty instance based on the provided slug or returns a 404 if not found.
        3. Processes POST requests to update the skill:
            a. Populates the SkillForm with POST data.
            b. If the form is valid, replaces the current skill with the new skill in the user's profile and redirects to the 'account' page with a success message.
        4. Initializes the SkillForm with the current skill for GET requests.
        5. Prepares the context with the form and the current skill.
        6. Renders the skill form template with the context.

    The context for rendering the template includes:
        - form: The SkillForm instance for updating the skill.
        - current_skill: The current Faculty instance being updated.

    Example:
        >>> updateSkill(request, 'Architecture')
    """
    profile = request.user.profile
    current_skill = get_object_or_404(Skill, slug=skill_slug)

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            new_skill = form.cleaned_data['skill']
            profile.skills.remove(current_skill)
            profile.skills.add(new_skill)
            messages.success(request, 'Faculty successfully updated')
            return redirect('account')
    else:
        form = SkillForm(initial={'skill': current_skill})

    context = {'form': form, 'current_skill': current_skill}
    return render(request, 'users/skill_form.html', context)



@login_required(login_url='login')
def deleteSkill(request, skill_slug):
    """
    Handles the view for deleting an existing faculty from the logged-in user's profile.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        skill_slug (str): The slug identifier for the faculty to be deleted.

    Returns:
        HttpResponse: The HTTP response object with the rendered delete confirmation template or a redirect to the user's account page.

    This view function performs the following tasks:
        1. Retrieves the profile of the logged-in user.
        2. Retrieves the faculty instance from the user's profile based on the provided slug.
        3. Processes POST requests to delete the skill:
            a. Removes the faculty from the user's profile.
            b. Redirects to the 'account' page with a success message.
        4. Prepares the context with the skill to be deleted.
        5. Renders the delete confirmation template with the context.

    The context for rendering the template includes:
        - object: The Faculty instance to be deleted.

    Example:
        >>> deleteSkill(request, 'Computer Sience')
    """
    profile = request.user.profile
    skill = profile.skills.get(slug=skill_slug)
    if request.method == 'POST':
        profile.skills.remove(skill)
        messages.success(request, 'Faculty successfully deleted')
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    """
    Handles the view for displaying the logged-in user's inbox with message requests.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object with the rendered inbox template.

    This view function performs the following tasks:
        1. Retrieves the profile of the logged-in user.
        2. Retrieves all message requests associated with the user's profile.
        3. Counts the number of unread message requests.
        4. Prepares the context with the message requests and the count of unread messages.
        5. Renders the inbox template with the context.

    The context for rendering the template includes:
        - messageRequests: A queryset of all message requests associated with the user's profile.
        - unreadCount: The count of unread message requests.

    Example:
        >>> inbox(request)
    """
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount }
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    """
    Handles the view for displaying a single message and marking it as read.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        pk (int): The primary key of the message to be viewed.

    Returns:
        HttpResponse: The HTTP response object with the rendered message template.

    This view function performs the following tasks:
        1. Retrieves the profile of the logged-in user.
        2. Retrieves the message instance associated with the user's profile and the provided primary key.
        3. If the message is unread, marks it as read and saves the change.
        4. Prepares the context with the message.
        5. Renders the message template with the context.

    The context for rendering the template includes:
        - message: The Message instance to be viewed.

    Example:
        >>> viewMessage(request, 1)
    """
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)

def createMessage(request, username):
    """
    Handles the creation and sending of a message to a specified user.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        username (str): The username of the recipient of the message.

    Returns:
        HttpResponse: The HTTP response object with the rendered message form template or a redirect to the recipient's profile page.

    This view function performs the following tasks:
        1. Retrieves the profile of the recipient based on the provided username.
        2. Initializes an empty MessageForm for GET requests.
        3. Tries to retrieve the profile of the sender (logged-in user):
            a. If the user is not logged in, sets the sender to None.
        4. Processes POST requests to create and send a message:
            a. Populates the MessageForm with POST data.
            b. If the form is valid, sets the sender, recipient, name, and email fields of the message and saves it.
            c. Displays a success message and redirects to the recipient's profile page.
        5. Prepares the context with the recipient's profile and the form.
        6. Renders the message form template with the context.

    The context for rendering the template includes:
        - recipient: The Profile instance of the message recipient.
        - form: The MessageForm instance for creating the message.

    Example:
        >>> createMessage(request, 'john_doe')
    """
    recipient = Profile.objects.get(username=username)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user_profile', username=recipient.username)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)


def contact(request):
    """
    Handles the view for displaying the contact page.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object with the rendered contact page template.

    This view function performs the following tasks:
        1. Renders the contact page template.

    Example:
        >>> contact(request)
    """
    return render(request, 'contacts.html')


def about_us(request):
    """
    Handles the view for displaying the "About Us" page.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object with the rendered "About Us" page template.

    This view function performs the following tasks:
        1. Renders the "About Us" page template.

    Example:
        >>> about_us(request)
    """
    return render(request, 'about_us.html')
