from django.db import models

# Create your models here.
class Question(models.Model):
    text = models.TextField("Текст вопроса")
    image = models.ImageField("Изображение", upload_to="questions/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]