from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import QuestionType, Question, Image, Answer, CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_researcher', 'is_admin', 'is_staff')
    list_filter = ('is_researcher', 'is_admin', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 
                      'is_researcher', 'is_admin', 
                      'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2',
                      'is_researcher', 'is_admin', 'is_staff'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

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