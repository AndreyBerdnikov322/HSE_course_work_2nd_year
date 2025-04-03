from django.contrib import admin
from .models import QuestionType, Question, Image, Answer  # Импортируем все модели
# Register your models here.

@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question_type', 'created_at')
    list_filter = ('question_type',)
    search_fields = ('text',)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('question', 'caption')
    raw_id_fields = ('question',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
    list_filter = ('is_correct',)