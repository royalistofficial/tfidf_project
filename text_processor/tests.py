# tests.py
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from django.urls import reverse
from .forms import UploadFileForm
from .models import UploadedText
from unittest.mock import patch

from text_processor.forms import UploadFileForm
from text_processor.models import UploadedText
class FormValidationTests(TestCase):
    def test_form_with_valid_files(self):
        files = [
            SimpleUploadedFile("test1.txt", b"test"),
            SimpleUploadedFile("test2.txt", b"test")
        ]
        form = UploadFileForm(files={'files': files})
        self.assertTrue(form.is_valid())

    def test_form_with_no_files(self):
        form = UploadFileForm(files={})
        self.assertFalse(form.is_valid())
        self.assertIn('files', form.errors)

    def test_form_with_invalid_file_type(self):
        file = SimpleUploadedFile("test.pdf", b"test")
        form = UploadFileForm(files={'files': [file]})
        self.assertFalse(form.is_valid())


class TextProcessorViewsTests(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('text_processor:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'text_processor/home.html')

    def test_upload_file_get_request(self):
        response = self.client.get(reverse('text_processor:upload'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UploadFileForm)
        self.assertTemplateUsed(response, 'text_processor/upload.html')

    def test_upload_file_valid_post_request(self):
        test_files = [
            SimpleUploadedFile("test1.txt", b"Sample content 1"),
            SimpleUploadedFile("test2.txt", b"Sample content 2")
        ]
        
        response = self.client.post(
            reverse('text_processor:upload'),
            {'files': test_files},
            format='multipart'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'text_processor/results.html')
        self.assertEqual(UploadedText.objects.count(), 2)
        self.assertIn('results', response.context)


    def test_unicode_decode_error_handling(self):
        binary_file = SimpleUploadedFile("test.bin", b"\x80invalid_utf8")
        
        response = self.client.post(
            reverse('text_processor:upload'),
            {'files': [binary_file]},
            format='multipart',
            follow=True
        )
        
        self.assertRedirects(response, reverse('text_processor:upload'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(UploadedText.objects.count(), 0)
        self.assertEqual(len(messages), 1)
        self.assertIn("Ошибка валидации формы", str(messages[0]))

    def test_file_processing_exception_handling(self):
        invalid_file = SimpleUploadedFile("test.txt", b"")
        invalid_file.content_type = 'text/plain'
        
        with patch(
            'text_processor.models.UploadedText.objects.create',
            side_effect=Exception("DB error")
        ):
            response = self.client.post(
                reverse('text_processor:upload'),
                {'files': [invalid_file]},
                format='multipart',
                follow=True
            )
            
            self.assertRedirects(response, reverse('text_processor:upload'))
            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertIn("Ошибка валидации формы", str(messages[0]))