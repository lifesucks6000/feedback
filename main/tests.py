from django.test import TestCase, Client
from django.urls import reverse
from .models import Feedback
from .forms import FeedbackForm


class FeedbackTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.feedback = Feedback.objects.create(
            name="Test User",
            message="Test feedback message"
        )
        self.list_url = reverse('feedback_list')
        self.create_url = reverse('feedback_form')
        self.edit_url = reverse('edit_feedback', args=[self.feedback.id])
        self.delete_url = reverse('delete_feedback', args=[self.feedback.id])

    def test_feedback_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback_list.html')

    def test_feedback_create_view(self):
        data = {
            'name': 'New User',
            'message': 'New feedback'
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Feedback.objects.filter(name='New User').exists())

    def test_feedback_edit_view(self):
        data = {
            'name': 'Updated User',
            'message': 'Updated feedback'
        }
        response = self.client.post(self.edit_url, data)
        self.assertEqual(response.status_code, 302)
        self.feedback.refresh_from_db()
        self.assertEqual(self.feedback.name, 'Updated User')
        self.assertEqual(self.feedback.message, 'Updated feedback')

    def test_feedback_delete_view(self):
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Feedback.objects.filter(id=self.feedback.id).exists())

    def test_feedback_form_valid(self):
        form_data = {
            'name': 'Test Name',
            'message': 'Test Message'
        }
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_feedback_form_invalid(self):
        form_data = {
            'name': '',  # name is required
            'message': 'Test Message'
        }
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_thank_you_page(self):
        response = self.client.get(reverse('thank_you'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thank_you.html')
