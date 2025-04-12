from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, Skill, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from captcha.models import CaptchaStore


class UsersViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser2', password='12345')
        cls.profile, created = Profile.objects.get_or_create(
            user=cls.user,
            defaults={
                'name': 'Test User2',
                'email': 'test2@example.com',
                'username': 'testuser2'
            }
        )
        cls.skill, created = Skill.objects.get_or_create(name='Python', slug='python')
        cls.profile.skills.add(cls.skill)
        cls.message, created = Message.objects.get_or_create(
            sender=cls.profile,
            recipient=cls.profile,
            subject='Test Subject',
            body='Test Body'
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser2', password='12345')

    def test_login_view(self):
        self.client.logout()
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login_register.html')

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_register_view(self):
        self.client.logout()
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login_register.html')

    def test_profiles_view(self):
        response = self.client.get(reverse('profiles'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profiles.html')

    def test_user_profile_view(self):
        response = self.client.get(reverse('user_profile', args=['testuser2']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_profile.html')

    def test_user_account_view(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/account.html')

    def test_edit_account_view(self):
        response = self.client.get(reverse('edit-account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_form.html')

    def test_create_skill_view(self):
        response = self.client.get(reverse('create-skill'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/skill_form.html')

    def test_update_skill_view(self):
        response = self.client.get(reverse('update-skill', args=['python']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/skill_form.html')

    def test_delete_skill_view(self):
        response = self.client.get(reverse('delete-skill', args=['python']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_template.html')

    def test_inbox_view(self):
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/inbox.html')

    def test_view_message_view(self):
        response = self.client.get(reverse('message', args=[self.message.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/message.html')

    def test_create_message_view(self):
        response = self.client.get(reverse('create-message', args=['testuser2']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/message_form.html')


class UsersFormsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser3', password='12345')
        cls.profile, created = Profile.objects.get_or_create(
            user=cls.user,
            defaults={
                'name': 'Test User3',
                'email': 'test3@example.com',
                'username': 'testuser3'
            }
        )

    def test_custom_user_creation_form(self):
        captcha_key = CaptchaStore.generate_key()
        captcha_value = CaptchaStore.objects.get(hashkey=captcha_key).response
        form_data = {
            'first_name': 'Test',
            'email': 'test@example.com',
            'username': 'testuser4',
            'password1': 'Acomplexpassword123',
            'password2': 'Acomplexpassword123',
            'captcha_0': captcha_key,
            'captcha_1': captcha_value,
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_profile_form(self):
        profile = Profile.objects.get(username='testuser3')
        form_data = {
            'name': 'Updated User',
            'email': 'updated@example.com',
            'username': 'updateduser',
            'bio': 'Updated bio',
            'intro': 'Updated intro',
            'instagram': 'updated_instagram',
            'facebook': 'updated_facebook'
        }
        form = ProfileForm(data=form_data, instance=profile)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_skill_form(self):
        skill = Skill.objects.create(name='Django', slug='django')
        form_data = {'skill': skill.id}
        form = SkillForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_message_form(self):
        form_data = {
            'name': 'Test Sender',
            'email': 'sender@example.com',
            'subject': 'Test Subject',
            'body': 'Test Body'
        }
        form = MessageForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")
