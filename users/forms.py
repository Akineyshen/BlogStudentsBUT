from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message
from django import forms
from captcha.fields import CaptchaField


class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for creating new users that includes a CAPTCHA field.

    Fields:
        captcha (CaptchaField): A CAPTCHA field for bot protection.

    Meta:
        model (User): The model associated with this form.
        fields (list): The fields included in the form: first_name, email, username, password1, password2, and captcha.
        labels (dict): Custom labels for the form fields.

    Methods:
        __init__(*args, **kwargs): Initializes the form with custom CSS classes for fields.
    """
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2', 'captcha']
        labels = {
            'first_name': 'Name',
        }

    def __init__(self, *args, **kwargs):
        """
        Initializes the form with custom CSS classes for each field.
        """
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    """
    A form for creating and updating Profile instances.

    Meta:
        model (Profile): The model associated with this form.
        fields (list): The fields included in the form: name, email, username, bio, intro, image, instagram, and facebook.

    Methods:
        __init__(*args, **kwargs): Initializes the form with custom CSS classes for fields.
    """
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username',
                  'bio', 'intro', 'image',
                  'instagram', 'facebook']

    def __init__(self, *args, **kwargs):
        """
        Initializes the form with custom CSS classes for each field.
        """
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class SkillForm(forms.Form):
    """
    A form for selecting a skill from available Skill instances.

    Fields:
        skill (ModelChoiceField): A field for selecting a skill from the Skill model's queryset, rendered as a select dropdown.

    Methods:
        __init__(*args, **kwargs): Initializes the form with custom CSS classes for fields.
    """
    skill = forms.ModelChoiceField(queryset=Skill.objects.all(), widget=forms.Select(attrs={'class': 'input'}), label='Faculty')

    def __init__(self, *args, **kwargs):
        """
        Initializes the form with custom CSS classes for each field.
        """
        super(SkillForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class MessageForm(ModelForm):
    """
    A form for creating and updating Message instances.

    Meta:
        model (Message): The model associated with this form.
        fields (list): The fields included in the form: name, email, subject, and body.

    Methods:
        __init__(*args, **kwargs): Initializes the form with custom CSS classes for fields.
    """
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        """
        Initializes the form with custom CSS classes for each field.
        """
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})