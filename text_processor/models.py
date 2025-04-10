from django.db import models

class UploadedText(models.Model):
    file = models.FileField(upload_to='uploads/', verbose_name="Текстовый файл")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    tf_data = models.JSONField(blank=True, null=True, verbose_name="TF данные")
    idf_data = models.JSONField(blank=True, null=True, verbose_name="IDF данные")
