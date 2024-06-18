from django.forms import ModelForm
from .models import Article, Review, Tag
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import format_html


class ArticleForm(ModelForm):
    """
    A form for creating and updating Article instances.

    Fields:
        tag (ModelChoiceField): A required field for selecting a category from available tags.

    Meta:
        model (Article): The model associated with this form.
        fields (list): The fields included in the form.
        labels (dict): Custom labels for the form fields.
        widgets (dict): Custom widgets for rendering the form fields.

    Methods:
        clean_slug(): Validates the uniqueness of the slug, excluding the current instance.
        clean(): Validates that a password is provided if the article is marked as private.
        __init__(*args, **kwargs): Initializes the form with custom CSS classes for fields.
    """
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(), empty_label=None, label="Category", required=True)

    class Meta:
        model = Article
        fields = ['title', 'slug', 'image', 'tag', 'description', 'source_link', 'is_private', 'password']
        labels = {
            'title': 'Title',
            'slug': 'Unique link',
            'image': 'Image',
            'description': 'Description',
            'source_link': 'Link to an additional source',
            'is_private': 'Make the article private',
            'password': '',
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 20, 'placeholder': 'Enter your description'}),
            'title': forms.TextInput(attrs={'placeholder': 'Enter your title'}),
            'slug': forms.TextInput(attrs={'placeholder': 'Enter your unique link'}),
            'image': forms.FileInput(attrs={'placeholder': 'Upload your image here'}),
            'source_link': forms.TextInput(attrs={'placeholder': 'Enter your source link'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter the password if the article is private', 'id': 'password-field-container'}),
            'is_private': forms.CheckboxInput(attrs={'id': 'is-private-checkbox', 'class': 'private-checkbox'}),
        }

    def clean_slug(self):
        """
        Validates the slug field to ensure it is unique, excluding the current instance.

        Returns:
            str: The cleaned slug value.

        Raises:
            ValidationError: If an article with the same slug already exists.
        """
        slug = self.cleaned_data['slug']
        article_id = self.instance.id if self.instance else None

        if Article.objects.filter(slug=slug).exclude(id=article_id).exists():
            raise ValidationError("An article with such a link already exists.")
        return slug

    def clean(self):
        """
        Validates the form fields, ensuring a password is provided if the article is private.

        Returns:
            dict: The cleaned data.

        Raises:
            ValidationError: If the article is private but no password is provided.
        """
        cleaned_data = super().clean()
        is_private = cleaned_data.get("is_private")
        password = cleaned_data.get("password")
        if is_private and not password:
            raise forms.ValidationError("Please enter a password for a private article.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        """
        Initializes the form with custom CSS classes for each field.
        """
        super(ArticleForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})




class ReviewForm(ModelForm):
    """
    A form for creating and updating Review instances.

    Meta:
        model (Review): The model associated with this form.
        fields (list): The fields included in the form, specifically the body of the review.
        labels (dict): Custom labels for the form fields.

    Methods:
        __init__(*args, **kwargs): Initializes the form with custom CSS classes for the body field.
    """
    class Meta:
        model = Review
        fields = ['body']
        labels = {
            'body': 'Edit your comment'
        }

    def __init__(self, *args, **kwargs):
        """
        Initializes the form with custom CSS classes for the body field.
        """
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({'class': 'input'})