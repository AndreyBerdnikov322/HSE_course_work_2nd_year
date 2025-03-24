from django import forms
from .models import Question
from django.forms import ClearableFileInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = "Удалить изображение"  # Новая надпись
    template_name = 'widgets/custom_image_input.html'  # Кастомный шаблон

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'image']
        widgets = {
            'image': CustomClearableFileInput(attrs={'class': 'form-control-file'})
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
        help_texts = {
            'username': 'Только буквы, цифры и символы @/./+/-/_',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }